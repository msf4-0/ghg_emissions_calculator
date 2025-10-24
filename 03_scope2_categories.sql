USE ghg_emissions_db;

-- SCOPE 2: INDIRECT ENERGY GHG EMISSIONS
-- Delete existing Scope 2 data to avoid duplicates
DELETE FROM ghg_categories WHERE scope_number = 2;

-- Purchased Electricity
INSERT INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES
(2, 'Indirect Energy GHG Emissions', 'S2-01', 'Purchased Electricity', 'S2-01-01', 'Grid Electricity UK (Average)', 0.19338000, 'kg CO2e/kWh', 'UK national grid electricity consumption'),
(2, 'Indirect Energy GHG Emissions', 'S2-01', 'Purchased Electricity', 'S2-01-02', 'Renewable Electricity (Certified)', 0.00000000, 'kg CO2e/kWh', 'Certified renewable electricity with REGOs'),
(2, 'Indirect Energy GHG Emissions', 'S2-01', 'Purchased Electricity', 'S2-01-03', 'Nuclear Electricity', 0.00000000, 'kg CO2e/kWh', 'Nuclear electricity generation'),
(2, 'Indirect Energy GHG Emissions', 'S2-01', 'Purchased Electricity', 'S2-01-04', 'Coal Electricity', 0.82000000, 'kg CO2e/kWh', 'Coal-fired electricity generation'),
(2, 'Indirect Energy GHG Emissions', 'S2-01', 'Purchased Electricity', 'S2-01-05', 'Natural Gas Electricity', 0.35000000, 'kg CO2e/kWh', 'Natural gas electricity generation'),
(2, 'Indirect Energy GHG Emissions', 'S2-01', 'Purchased Electricity', 'S2-01-06', 'Solar Electricity', 0.04800000, 'kg CO2e/kWh', 'Solar photovoltaic electricity'),
(2, 'Indirect Energy GHG Emissions', 'S2-01', 'Purchased Electricity', 'S2-01-07', 'Wind Electricity', 0.01100000, 'kg CO2e/kWh', 'Wind turbine electricity generation'),

-- Purchased Heat, Steam, and Cooling
(2, 'Indirect Energy GHG Emissions', 'S2-02', 'Purchased Heat/Steam/Cooling', 'S2-02-01', 'District Heating', 0.21233000, 'kg CO2e/kWh', 'Purchased district heating systems'),
(2, 'Indirect Energy GHG Emissions', 'S2-02', 'Purchased Heat/Steam/Cooling', 'S2-02-02', 'Purchased Steam (Industrial)', 0.18385000, 'kg CO2e/kWh', 'Industrial steam purchase'),
(2, 'Indirect Energy GHG Emissions', 'S2-02', 'Purchased Heat/Steam/Cooling', 'S2-02-03', 'District Cooling', 0.15000000, 'kg CO2e/kWh', 'Purchased district cooling systems'),
(2, 'Indirect Energy GHG Emissions', 'S2-02', 'Purchased Heat/Steam/Cooling', 'S2-02-04', 'Biomass District Heating', 0.03000000, 'kg CO2e/kWh', 'Biomass-based district heating'),
(2, 'Indirect Energy GHG Emissions', 'S2-02', 'Purchased Heat/Steam/Cooling', 'S2-02-05', 'Geothermal Heating', 0.01200000, 'kg CO2e/kWh', 'Geothermal heating systems'),
(2, 'Indirect Energy GHG Emissions', 'S2-02', 'Purchased Heat/Steam/Cooling', 'S2-02-06', 'Heat Pumps (Electric)', 0.05801000, 'kg CO2e/kWh', 'Electric heat pump systems');
