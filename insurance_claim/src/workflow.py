from llama_index.core.workflow import Event, StartEvent, StopEvent, Context, Workflow, step
from llama_index.core.prompts import ChatPromptTemplate
from .models import ClaimInfo, PolicyQueries, PolicyRecommendation, ClaimDecision
from .prompts import GENERATE_POLICY_QUERIES_PROMPT, POLICY_RECOMMENDATION_PROMPT
from .utils import parse_claim_from_text
from .config import policy_retriever, get_declarations_docs, llm

# Define Workflow Events
class ClaimInfoEvent(Event):
    def __init__(self, claim_info: ClaimInfo):
        self.claim_info = claim_info


class PolicyQueryEvent(Event):
    def __init__(self, queries: PolicyQueries):
        self.queries = queries


class PolicyMatchedEvent(Event):
    def __init__(self, policy_text: str):
        self.policy_text = policy_text


class RecommendationEvent(Event):
    def __init__(self, recommendation: PolicyRecommendation):
        self.recommendation = recommendation


class DecisionEvent(Event):
    def __init__(self, decision: ClaimDecision):
        self.decision = decision


class LogEvent(Event):
    def __init__(self, msg: str, delta: bool = False):
        self.msg = msg
        self.delta = delta


# Define the Workflow
class AutoInsuranceWorkflow(Workflow):
    """
    Workflow to process an auto insurance claim and generate a recommendation.
    """
    def __init__(self, policy_retriever, llm, output_dir: str = "data_out", **kwargs) -> None:
        super().__init__(**kwargs)
        self.policy_retriever = policy_retriever
        self.llm = llm

    @step
    async def load_claim_info(self, ctx: Context, ev: StartEvent) -> ClaimInfoEvent:
        claim_info = parse_claim_from_text(ev.claim_json_text)
        await ctx.set("claim_info", claim_info)
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=f"Loaded claim info for {claim_info.claim_number}"))
        return ClaimInfoEvent(claim_info=claim_info)

    @step
    async def generate_policy_queries(self, ctx: Context, ev: ClaimInfoEvent) -> PolicyQueryEvent:
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=">> Generating Policy Queries"))
        prompt = ChatPromptTemplate.from_messages([("user", GENERATE_POLICY_QUERIES_PROMPT)])
        queries = await self.llm.astructured_predict(
            PolicyQueries,
            prompt,
            claim_info=ev.claim_info.model_dump_json()
        )
        return PolicyQueryEvent(queries=queries)

    @step
    async def retrieve_policy_text(self, ctx: Context, ev: PolicyQueryEvent) -> PolicyMatchedEvent:
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=">> Retrieving policy sections"))
        claim_info = await ctx.get("claim_info")
        combined_docs = {}
        for query in ev.queries.queries:
            if self._verbose:
                ctx.write_event_to_stream(LogEvent(msg=f">> Query: {query}"))
            docs = await self.policy_retriever.aretrieve(query)
            for d in docs:
                combined_docs[d.id_] = d

        # Fetch the declarations page for the policy holder
        d_doc = get_declarations_docs(claim_info.policy_number)[0]
        combined_docs[d_doc.id_] = d_doc

        policy_text = "\n\n".join([doc.get_content() for doc in combined_docs.values()])
        await ctx.set("policy_text", policy_text)
        return PolicyMatchedEvent(policy_text=policy_text)

    @step
    async def generate_recommendation(self, ctx: Context, ev: PolicyMatchedEvent) -> RecommendationEvent:
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=">> Generating Policy Recommendation"))
        claim_info = await ctx.get("claim_info")
        prompt = ChatPromptTemplate.from_messages([("user", POLICY_RECOMMENDATION_PROMPT)])
        recommendation = await self.llm.astructured_predict(
            PolicyRecommendation,
            prompt,
            claim_info=claim_info.model_dump_json(),
            policy_text=ev.policy_text
        )
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=f">> Recommendation: {recommendation.model_dump_json()}"))
        return RecommendationEvent(recommendation=recommendation)

    @step
    async def finalize_decision(self, ctx: Context, ev: RecommendationEvent) -> DecisionEvent:
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=">> Finalizing Decision"))
        claim_info = await ctx.get("claim_info")
        rec = ev.recommendation
        covered = "covered" in rec.recommendation_summary.lower() or (
            rec.settlement_amount is not None and rec.settlement_amount > 0
        )
        deductible = rec.deductible if rec.deductible is not None else 0.0
        recommended_payout = rec.settlement_amount if rec.settlement_amount else 0.0
        decision = ClaimDecision(
            claim_number=claim_info.claim_number,
            covered=covered,
            deductible=deductible,
            recommended_payout=recommended_payout,
            notes=rec.recommendation_summary
        )
        return DecisionEvent(decision=decision)

    @step
    async def output_result(self, ctx: Context, ev: DecisionEvent) -> StopEvent:
        if self._verbose:
            ctx.write_event_to_stream(LogEvent(msg=f">> Decision: {ev.decision.model_dump_json()}"))
        return StopEvent(result={"decision": ev.decision})