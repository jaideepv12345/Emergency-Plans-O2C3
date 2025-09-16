# Data Creation Methodology

This document outlines the methodology used to create the synthetic data for the World Bank emergency management project in Thane district, Maharashtra, India.

## Data Variables

1. **Response Time**: Measured in minutes from initial alert to emergency service arrival at affected site.
   - Baseline (2012): Range of 32-53 minutes across areas
   - Post-Intervention (2014): Range of 19-32 minutes across areas
   - Target reduction: 40% from baseline

2. **Preparedness Score**: Composite index (0-100) based on the City Resilience Index framework:
   - Infrastructure readiness (25%)
   - Community knowledge levels (25%)
   - Coordination effectiveness (25%)
   - Resource availability (25%)
   - Baseline (2012): Range of 28-46 across areas
   - Post-Intervention (2014): Range of 36-55 across areas
   - Target improvement: 20% from baseline

3. **Community Engagement**:
   - Population: Actual population figures based on Maharashtra census data
   - Participation: Percentage of population participating in drills (target: 60%)
   - Drills: 1-2 drills per area, with 20 total drills across all areas

## Data Creation Approach

The synthetic data was created to realistically represent the impact of the O2C3 protocol implementation and community-led disaster drills, while accounting for:

1. **Area Size Variation**: Larger areas typically had more resources but greater coordination challenges
2. **Geographical Factors**: Areas prone to flooding, landslides, or with informal settlements had different baseline preparedness levels
3. **Implementation Intensity**: Areas with two drills showed greater improvements than those with one
4. **Resource Allocation**: District centers and larger areas received more intensive interventions

## Statistical Considerations

1. **Normal Distribution**: Response times and preparedness scores were modeled to follow approximately normal distributions
2. **Correlation Factors**: Negative correlation between area size and response time improvement (larger areas showed less dramatic percentage improvements)
3. **Intervention Effect**: Modeled using a modified dose-response relationship where multiple drills produced diminishing returns

This methodology ensures the data realistically represents the claimed 40% reduction in response time and 20% improvement in preparedness scores while maintaining internal consistency and plausibility.
