USE ghg_emissions_db;

-- SCOPE 1: DIRECT GHG EMISSIONS
-- Delete existing Scope 1 data to avoid duplicates
DELETE FROM ghg_categories WHERE scope_number = 1;

-- Stationary Combustion
INSERT INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES
(1, 'Direct GHG Emissions', 'S1-01', 'Stationary Combustion', 'S1-01-01', 'Natural Gas', 0.18385000, 'kg CO2e/kWh', 'Natural gas combustion in boilers, furnaces, and heating systems'),
(1, 'Direct GHG Emissions', 'S1-01', 'Stationary Combustion', 'S1-01-02', 'Coal', 0.34224000, 'kg CO2e/kWh', 'Coal combustion in power generation and heating'),
(1, 'Direct GHG Emissions', 'S1-01', 'Stationary Combustion', 'S1-01-03', 'Gas Oil/Diesel', 0.24651000, 'kg CO2e/litre', 'Gas oil and diesel combustion in generators'),
(1, 'Direct GHG Emissions', 'S1-01', 'Stationary Combustion', 'S1-01-04', 'LPG (Liquefied Petroleum Gas)', 0.21449000, 'kg CO2e/litre', 'LPG combustion in heating and cooking'),
(1, 'Direct GHG Emissions', 'S1-01', 'Stationary Combustion', 'S1-01-05', 'Fuel Oil (Heavy)', 0.26821000, 'kg CO2e/litre', 'Heavy fuel oil combustion in boilers'),
(1, 'Direct GHG Emissions', 'S1-01', 'Stationary Combustion', 'S1-01-06', 'Biomass (Wood Pellets)', 0.01517000, 'kg CO2e/kg', 'Wood pellets and biomass combustion'),
(1, 'Direct GHG Emissions', 'S1-01', 'Stationary Combustion', 'S1-01-07', 'Kerosene', 0.24651000, 'kg CO2e/litre', 'Kerosene combustion in heating systems'),

-- Mobile Combustion
(1, 'Direct GHG Emissions', 'S1-02', 'Mobile Combustion', 'S1-02-01', 'Petrol Cars (Average)', 0.16743000, 'kg CO2e/litre', 'Petrol vehicles in company fleet'),
(1, 'Direct GHG Emissions', 'S1-02', 'Mobile Combustion', 'S1-02-02', 'Diesel Cars (Average)', 0.16901000, 'kg CO2e/litre', 'Diesel vehicles in company fleet'),
(1, 'Direct GHG Emissions', 'S1-02', 'Mobile Combustion', 'S1-02-03', 'HGV Diesel (Heavy Goods)', 0.17172000, 'kg CO2e/litre', 'Heavy goods vehicles and trucks'),
(1, 'Direct GHG Emissions', 'S1-02', 'Mobile Combustion', 'S1-02-04', 'Aviation Fuel (Jet A1)', 0.24651000, 'kg CO2e/litre', 'Company aircraft and private jets'),
(1, 'Direct GHG Emissions', 'S1-02', 'Mobile Combustion', 'S1-02-05', 'Marine Gas Oil', 0.26567000, 'kg CO2e/litre', 'Marine vessel fuel for company boats'),
(1, 'Direct GHG Emissions', 'S1-02', 'Mobile Combustion', 'S1-02-06', 'Motorcycles', 0.11449000, 'kg CO2e/litre', 'Company motorcycles and scooters'),
(1, 'Direct GHG Emissions', 'S1-02', 'Mobile Combustion', 'S1-02-07', 'LGV Diesel (Light Goods)', 0.16901000, 'kg CO2e/litre', 'Light goods vehicles and vans'),

-- Process Emissions
(1, 'Direct GHG Emissions', 'S1-03', 'Process Emissions', 'S1-03-01', 'Cement Production', 0.52500000, 'kg CO2e/kg', 'CO2 from cement manufacturing process'),
(1, 'Direct GHG Emissions', 'S1-03', 'Process Emissions', 'S1-03-02', 'Steel Production', 2.30000000, 'kg CO2e/kg', 'CO2 from steel manufacturing process'),
(1, 'Direct GHG Emissions', 'S1-03', 'Process Emissions', 'S1-03-03', 'Aluminum Production', 11.46000000, 'kg CO2e/kg', 'CO2 from aluminum smelting process'),
(1, 'Direct GHG Emissions', 'S1-03', 'Process Emissions', 'S1-03-04', 'Chemical Processes', 1.00000000, 'kg CO2e/unit', 'Various chemical manufacturing processes'),
(1, 'Direct GHG Emissions', 'S1-03', 'Process Emissions', 'S1-03-05', 'Glass Production', 0.83000000, 'kg CO2e/kg', 'CO2 from glass manufacturing'),
(1, 'Direct GHG Emissions', 'S1-03', 'Process Emissions', 'S1-03-06', 'Lime Production', 0.78500000, 'kg CO2e/kg', 'CO2 from lime manufacturing'),

-- Fugitive Emissions
(1, 'Direct GHG Emissions', 'S1-04', 'Fugitive Emissions', 'S1-04-01', 'HFC Refrigerants (R-134a)', 1430.00000000, 'kg CO2e/kg', 'HFC refrigerant leakage from HVAC systems'),
(1, 'Direct GHG Emissions', 'S1-04', 'Fugitive Emissions', 'S1-04-02', 'Natural Gas Leaks (Methane)', 25.00000000, 'kg CO2e/kg', 'Methane leakage from equipment and pipelines'),
(1, 'Direct GHG Emissions', 'S1-04', 'Fugitive Emissions', 'S1-04-03', 'CO2 Fire Suppression', 1.00000000, 'kg CO2e/kg', 'CO2 from fire suppression systems'),
(1, 'Direct GHG Emissions', 'S1-04', 'Fugitive Emissions', 'S1-04-04', 'SF6 Electrical Equipment', 22800.00000000, 'kg CO2e/kg', 'SF6 leakage from electrical equipment'),
(1, 'Direct GHG Emissions', 'S1-04', 'Fugitive Emissions', 'S1-04-05', 'HFC Refrigerants (R-410A)', 2088.00000000, 'kg CO2e/kg', 'R-410A refrigerant leakage'),
(1, 'Direct GHG Emissions', 'S1-04', 'Fugitive Emissions', 'S1-04-06', 'Nitrous Oxide (N2O)', 298.00000000, 'kg CO2e/kg', 'N2O emissions from industrial processes');
