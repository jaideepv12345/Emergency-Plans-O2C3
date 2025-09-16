# R Code for Statistical Analysis of Emergency Management Project
# Thane District, Maharashtra, India (2012-2014)

# Load required libraries
library(tidyverse)
library(ggplot2)
library(gridExtra)
library(scales)

# Set working directory if needed
# setwd("/path/to/your/directory")

# Read the data
baseline_data <- read.csv("../data/baseline_data.csv")
post_intervention_data <- read.csv("../data/post_intervention_data.csv")

# Merge datasets
merged_data <- merge(baseline_data, post_intervention_data, 
                    by = c("Zone", "Area", "Area_ID", "Population"))

# Calculate key metrics
merged_data <- merged_data %>%
  mutate(
    Response_Time_Reduction = Baseline_Response_Time_Minutes - Post_Response_Time_Minutes,
    Response_Time_Reduction_Percent = (Response_Time_Reduction / Baseline_Response_Time_Minutes) * 100,
    Preparedness_Score_Improvement = Post_Preparedness_Score - Baseline_Preparedness_Score,
    Preparedness_Score_Improvement_Percent = (Preparedness_Score_Improvement / Baseline_Preparedness_Score) * 100,
    Participation_Rate = (Participants / Population) * 100
  )

# Display summary statistics
summary_stats <- merged_data %>%
  summarise(
    Mean_Baseline_Response_Time = mean(Baseline_Response_Time_Minutes),
    Mean_Post_Response_Time = mean(Post_Response_Time_Minutes),
    Mean_Response_Time_Reduction_Percent = mean(Response_Time_Reduction_Percent),
    Mean_Baseline_Preparedness = mean(Baseline_Preparedness_Score),
    Mean_Post_Preparedness = mean(Post_Preparedness_Score),
    Mean_Preparedness_Improvement_Percent = mean(Preparedness_Score_Improvement_Percent),
    Mean_Participation_Rate = mean(Participation_Rate),
    Total_Population = sum(Population),
    Total_Participants = sum(Participants),
    Total_Drills = sum(Drills_Conducted)
  )

print(summary_stats)

# Calculate zone-level statistics
zone_stats <- merged_data %>%
  group_by(Zone) %>%
  summarise(
    Response_Time_Reduction_Percent = mean(Response_Time_Reduction_Percent),
    Preparedness_Score_Improvement_Percent = mean(Preparedness_Score_Improvement_Percent),
    Participation_Rate = mean(Participation_Rate),
    Population = sum(Population),
    Participants = sum(Participants),
    Drills_Conducted = sum(Drills_Conducted)
  )

print(zone_stats)

# Perform paired t-test for response time reduction
response_time_ttest <- t.test(merged_data$Baseline_Response_Time_Minutes, 
                             merged_data$Post_Response_Time_Minutes, 
                             paired = TRUE)
print("T-Test for Response Time Reduction:")
print(response_time_ttest)

# Perform paired t-test for preparedness score improvement
preparedness_ttest <- t.test(merged_data$Baseline_Preparedness_Score, 
                            merged_data$Post_Preparedness_Score, 
                            paired = TRUE)
print("T-Test for Preparedness Score Improvement:")
print(preparedness_ttest)

# Calculate confidence intervals
response_time_ci <- t.test(merged_data$Response_Time_Reduction_Percent)$conf.int
preparedness_ci <- t.test(merged_data$Preparedness_Score_Improvement_Percent)$conf.int

print("95% Confidence Interval for Response Time Reduction (%):")
print(response_time_ci)

print("95% Confidence Interval for Preparedness Score Improvement (%):")
print(preparedness_ci)

# Correlation analysis
correlation_vars <- merged_data %>%
  select(Population, Response_Time_Reduction_Percent, 
         Preparedness_Score_Improvement_Percent, 
         Participation_Rate, Drills_Conducted)

correlation_matrix <- cor(correlation_vars)
print("Correlation Matrix:")
print(correlation_matrix)

# Create visualizations

# 1. Response Time Reduction by Zone
response_time_plot <- ggplot() +
  geom_bar(data = zone_stats, aes(x = Zone, y = Response_Time_Reduction_Percent), 
           stat = "identity", fill = "steelblue") +
  geom_hline(yintercept = 40, linetype = "dashed", color = "red") +
  geom_text(aes(x = 1.5, y = 42, label = "Target (40%)"), color = "red") +
  labs(title = "Response Time Reduction by Zone (%)",
       y = "Reduction Percentage",
       x = "Zone") +
  theme_minimal() +
  ylim(0, 50)

# 2. Preparedness Score Improvement by Zone
preparedness_plot <- ggplot() +
  geom_bar(data = zone_stats, aes(x = Zone, y = Preparedness_Score_Improvement_Percent), 
           stat = "identity", fill = "darkgreen") +
  geom_hline(yintercept = 20, linetype = "dashed", color = "red") +
  geom_text(aes(x = 1.5, y = 22, label = "Target (20%)"), color = "red") +
  labs(title = "Preparedness Score Improvement by Zone (%)",
       y = "Improvement Percentage",
       x = "Zone") +
  theme_minimal() +
  ylim(0, 30)

# 3. Scatter plot of drills vs response time reduction
drills_impact_plot <- ggplot(merged_data, aes(x = Drills_Conducted, y = Response_Time_Reduction_Percent)) +
  geom_point(size = 3, alpha = 0.7) +
  geom_smooth(method = "lm", se = TRUE, color = "blue") +
  labs(title = "Impact of Drill Frequency on Response Time Reduction",
       x = "Number of Drills Conducted",
       y = "Response Time Reduction (%)") +
  theme_minimal()

# 4. Before-After Comparison
# Prepare data for before-after plot
before_after_data <- data.frame(
  Time_Period = rep(c("Baseline (2012)", "Post-Intervention (2014)"), 2),
  Metric = c(rep("Response Time (min)", 2), rep("Preparedness Score", 2)),
  Value = c(mean(merged_data$Baseline_Response_Time_Minutes), 
            mean(merged_data$Post_Response_Time_Minutes),
            mean(merged_data$Baseline_Preparedness_Score), 
            mean(merged_data$Post_Preparedness_Score))
)

before_after_plot <- ggplot(before_after_data, aes(x = Time_Period, y = Value, fill = Metric)) +
  geom_bar(stat = "identity", position = "dodge") +
  facet_wrap(~Metric, scales = "free_y") +
  labs(title = "Before-After Comparison of Key Metrics",
       x = "",
       y = "Value") +
  theme_minimal() +
  scale_fill_manual(values = c("Response Time (min)" = "steelblue", 
                              "Preparedness Score" = "darkgreen"))

# 5. Participation Rate by Zone
participation_plot <- ggplot() +
  geom_bar(data = zone_stats, aes(x = Zone, y = Participation_Rate), 
           stat = "identity", fill = "orange") +
  labs(title = "Community Participation Rate by Zone (%)",
       y = "Participation Rate (%)",
       x = "Zone") +
  theme_minimal() +
  ylim(0, 70)

# Save plots
ggsave("../reports/r_response_time_reduction.png", response_time_plot, width = 8, height = 6)
ggsave("../reports/r_preparedness_improvement.png", preparedness_plot, width = 8, height = 6)
ggsave("../reports/r_drills_impact.png", drills_impact_plot, width = 8, height = 6)
ggsave("../reports/r_before_after_comparison.png", before_after_plot, width = 10, height = 6)
ggsave("../reports/r_participation_rate.png", participation_plot, width = 8, height = 6)

# Additional statistical analysis

# Effect size calculation (Cohen's d)
# For Response Time
mean_diff_response <- mean(merged_data$Response_Time_Reduction)
sd_diff_response <- sd(merged_data$Response_Time_Reduction)
cohens_d_response <- mean_diff_response / sd_diff_response

# For Preparedness Score
mean_diff_prep <- mean(merged_data$Preparedness_Score_Improvement)
sd_diff_prep <- sd(merged_data$Preparedness_Score_Improvement)
cohens_d_prep <- mean_diff_prep / sd_diff_prep

print("Effect Size (Cohen's d) for Response Time Reduction:")
print(cohens_d_response)
print("Effect Size (Cohen's d) for Preparedness Score Improvement:")
print(cohens_d_prep)

# Regression analysis: Impact of drills on response time reduction
drill_impact_model <- lm(Response_Time_Reduction_Percent ~ Drills_Conducted, data = merged_data)
print("Regression Analysis: Impact of Drills on Response Time Reduction")
print(summary(drill_impact_model))

# Regression analysis: Impact of participation rate on preparedness improvement
participation_impact_model <- lm(Preparedness_Score_Improvement_Percent ~ Participation_Rate, 
                                data = merged_data)
print("Regression Analysis: Impact of Participation Rate on Preparedness Improvement")
print(summary(participation_impact_model))

# Multiple regression: Combined factors influencing response time reduction
multi_model <- lm(Response_Time_Reduction_Percent ~ Drills_Conducted + Participation_Rate + 
                 Population + Baseline_Preparedness_Score, data = merged_data)
print("Multiple Regression: Factors Influencing Response Time Reduction")
print(summary(multi_model))

# Calculate overall achievement against targets
target_response_reduction <- 40
actual_response_reduction <- mean(merged_data$Response_Time_Reduction_Percent)
response_achievement <- (actual_response_reduction / target_response_reduction) * 100

target_preparedness_improvement <- 20
actual_preparedness_improvement <- mean(merged_data$Preparedness_Score_Improvement_Percent)
preparedness_achievement <- (actual_preparedness_improvement / target_preparedness_improvement) * 100

print(paste("Response Time Reduction Target Achievement:", round(response_achievement, 1), "%"))
print(paste("Preparedness Score Improvement Target Achievement:", round(preparedness_achievement, 1), "%"))

# Save the merged dataset for future reference
write.csv(merged_data, "../analysis/merged_data_with_calculations.csv", row.names = FALSE)

# Print final summary message
cat("\nStatistical analysis completed successfully.\n")
cat("Overall response time reduction:", round(mean(merged_data$Response_Time_Reduction_Percent), 2), "%\n")
cat("Overall preparedness score improvement:", round(mean(merged_data$Preparedness_Score_Improvement_Percent), 2), "%\n")
cat("Total population covered:", sum(merged_data$Population), "\n")
cat("Total participants:", sum(merged_data$Participants), "\n")
cat("Total drills conducted:", sum(merged_data$Drills_Conducted), "\n")
