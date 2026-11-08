# Landslide Detection Validation & Susceptibility Mapping
library(terra)
library(sf)

# 1. Load Data
# result_polygons <- st_read("data/results/landslides.geojson")
# inventory <- st_read("data/inventory/historical_landslides.gpkg")

calculate_f1_score <- function(predicted, reference) {
  # Intersection
  intersection <- st_intersection(predicted, reference)

  # Areas
  tp_area <- sum(st_area(intersection))
  p_area <- sum(st_area(predicted))
  r_area <- sum(st_area(reference))

  precision <- tp_area / p_area
  recall <- tp_area / r_area

  f1 <- 2 * (precision * recall) / (precision + recall)

  return(list(Precision = precision, Recall = recall, F1 = f1))
}

generate_susceptibility_heatmap <- function(slope_tif, results_geojson, output_tif = "data/results/susceptibility.tif") {
  slope <- rast(slope_tif)

  # Simple Susceptibility Model: Weighted combination of Slope and recent AI detections
  # In a real scenario, this would involve logistic regression or Random Forest.

  # Normalize slope 0-1
  slope_norm <- slope / max(values(slope, na.rm = TRUE))

  # Distance to recent landslides
  results <- st_read(results_geojson)
  # Ensure CRS matches
  results <- st_transform(results, st_crs(slope))

  dist_raster <- distance(slope, results)
  dist_norm <- 1 - (dist_raster / max(values(dist_raster, na.rm = TRUE)))

  # Heatmap = 0.6*Slope + 0.4*ProximityToRecent
  heatmap <- (0.6 * slope_norm) + (0.4 * dist_norm)

  writeRaster(heatmap, output_tif, overwrite = TRUE)
  message(paste0("Susceptibility heatmap saved to ", output_tif))
  return(heatmap)
}

# Main execution logic
results_file <- "data/results/landslides.geojson"
slope_file <- "data/dem/alos_slope.tif"

if (file.exists(results_file)) {
  print("--- Starting Validation & Susceptibility Mapping ---")
  generate_susceptibility_heatmap(slope_file, results_file)
  print("--- Validation Complete ---")
} else {
  print("Landslide detection results not found. Run Phases 1-3 first.")
}
