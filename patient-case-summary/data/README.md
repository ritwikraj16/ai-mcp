# Sample Patient Data

This directory contains sample patient data files in FHIR format.

## Data Sources

The sample data is generated using [Synthea](https://github.com/synthetichealth/synthea), a synthetic patient generator that creates realistic but not real patient data.

## Available Samples

- `almeta_buckridge.json`: A pediatric patient with asthma and atopic dermatitis

## How to Generate More Samples

To generate more sample data:

1. Clone the Synthea repository:
```bash
git clone https://github.com/synthetichealth/synthea.git
```

2. Build Synthea:
```bash
cd synthea
./gradlew build
```

3. Generate sample patients:
```bash
./run_synthea -p 10  # Generates 10 patients
```

4. Find the generated data in the `output/fhir` directory 

