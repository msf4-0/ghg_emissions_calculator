USE ghg_emissions_db;

-- SCOPE 3: OTHER INDIRECT GHG EMISSIONS
-- Delete existing Scope 3 data to avoid duplicates
DELETE FROM ghg_categories WHERE scope_number = 3;

-- Category 1: Purchased Goods and Services
INSERT INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES
(3, 'Other Indirect GHG Emissions', 'S3-01', 'Purchased Goods and Services', 'S3-01-01', 'Paper Products (Office)', 0.91000000, 'kg CO2e/kg', 'Office paper and stationery consumption'),
(3, 'Other Indirect GHG Emissions', 'S3-01', 'Purchased Goods and Services', 'S3-01-02', 'IT Equipment (Computers)', 300.00000000, 'kg CO2e/unit', 'Computers, laptops, and IT hardware'),
(3, 'Other Indirect GHG Emissions', 'S3-01', 'Purchased Goods and Services', 'S3-01-03', 'Office Furniture', 45.00000000, 'kg CO2e/unit', 'Desks, chairs, and office furniture'),
(3, 'Other Indirect GHG Emissions', 'S3-01', 'Purchased Goods and Services', 'S3-01-04', 'Cleaning Services', 2.50000000, 'kg CO2e/hour', 'Professional cleaning services'),
(3, 'Other Indirect GHG Emissions', 'S3-01', 'Purchased Goods and Services', 'S3-01-05', 'Catering Services', 3.20000000, 'kg CO2e/meal', 'Food and catering services'),
(3, 'Other Indirect GHG Emissions', 'S3-01', 'Purchased Goods and Services', 'S3-01-06', 'Professional Services', 0.15000000, 'kg CO2e/£', 'Consultancy, legal, accounting services'),
(3, 'Other Indirect GHG Emissions', 'S3-01', 'Purchased Goods and Services', 'S3-01-07', 'Marketing Materials', 1.20000000, 'kg CO2e/kg', 'Printed marketing and promotional materials'),
(3, 'Other Indirect GHG Emissions', 'S3-01', 'Purchased Goods and Services', 'S3-01-08', 'Textiles and Clothing', 8.50000000, 'kg CO2e/kg', 'Uniforms and corporate clothing'),

-- Category 2: Capital Goods
(3, 'Other Indirect GHG Emissions', 'S3-02', 'Capital Goods', 'S3-02-01', 'Buildings Construction', 500.00000000, 'kg CO2e/m²', 'New building construction and fit-out'),
(3, 'Other Indirect GHG Emissions', 'S3-02', 'Capital Goods', 'S3-02-02', 'Manufacturing Equipment', 2500.00000000, 'kg CO2e/unit', 'Industrial machinery and equipment'),
(3, 'Other Indirect GHG Emissions', 'S3-02', 'Capital Goods', 'S3-02-03', 'Vehicles Purchase', 15000.00000000, 'kg CO2e/unit', 'Company vehicle purchases'),
(3, 'Other Indirect GHG Emissions', 'S3-02', 'Capital Goods', 'S3-02-04', 'IT Infrastructure', 800.00000000, 'kg CO2e/unit', 'Servers, network equipment, data centers'),
(3, 'Other Indirect GHG Emissions', 'S3-02', 'Capital Goods', 'S3-02-05', 'Building Renovations', 250.00000000, 'kg CO2e/m²', 'Office renovations and refurbishments'),

-- Category 3: Fuel and Energy Related Activities (not in Scope 1 or 2)
(3, 'Other Indirect GHG Emissions', 'S3-03', 'Fuel and Energy Related Activities', 'S3-03-01', 'Upstream Electricity', 0.03466000, 'kg CO2e/kWh', 'Electricity transmission and distribution losses'),
(3, 'Other Indirect GHG Emissions', 'S3-03', 'Fuel and Energy Related Activities', 'S3-03-02', 'Upstream Natural Gas', 0.03685000, 'kg CO2e/kWh', 'Natural gas extraction and transportation'),
(3, 'Other Indirect GHG Emissions', 'S3-03', 'Fuel and Energy Related Activities', 'S3-03-03', 'Upstream Diesel', 0.05651000, 'kg CO2e/litre', 'Diesel extraction, refining, and transport'),
(3, 'Other Indirect GHG Emissions', 'S3-03', 'Fuel and Energy Related Activities', 'S3-03-04', 'Upstream Petrol', 0.05343000, 'kg CO2e/litre', 'Petrol extraction, refining, and transport'),
(3, 'Other Indirect GHG Emissions', 'S3-03', 'Fuel and Energy Related Activities', 'S3-03-05', 'Upstream Coal', 0.04500000, 'kg CO2e/kWh', 'Coal extraction and transportation'),

-- Category 4: Upstream Transportation and Distribution
(3, 'Other Indirect GHG Emissions', 'S3-04', 'Upstream Transportation and Distribution', 'S3-04-01', 'Road Freight (HGV)', 0.11449000, 'kg CO2e/tonne.km', 'Goods transport by heavy goods vehicles'),
(3, 'Other Indirect GHG Emissions', 'S3-04', 'Upstream Transportation and Distribution', 'S3-04-02', 'Rail Freight', 0.02567000, 'kg CO2e/tonne.km', 'Goods transport by rail'),
(3, 'Other Indirect GHG Emissions', 'S3-04', 'Upstream Transportation and Distribution', 'S3-04-03', 'Sea Freight (Container)', 0.01132000, 'kg CO2e/tonne.km', 'Goods transport by container ship'),
(3, 'Other Indirect GHG Emissions', 'S3-04', 'Upstream Transportation and Distribution', 'S3-04-04', 'Air Freight', 0.60200000, 'kg CO2e/tonne.km', 'Goods transport by air cargo'),
(3, 'Other Indirect GHG Emissions', 'S3-04', 'Upstream Transportation and Distribution', 'S3-04-05', 'Van Delivery (LGV)', 0.18500000, 'kg CO2e/tonne.km', 'Light goods vehicle delivery'),

-- Category 5: Waste Generated in Operations
(3, 'Other Indirect GHG Emissions', 'S3-05', 'Waste Generated in Operations', 'S3-05-01', 'Landfill Waste (Mixed)', 0.45751000, 'kg CO2e/kg', 'Mixed waste sent to landfill'),
(3, 'Other Indirect GHG Emissions', 'S3-05', 'Waste Generated in Operations', 'S3-05-02', 'Recycled Materials', 0.02077000, 'kg CO2e/kg', 'Recycled paper, plastic, metal'),
(3, 'Other Indirect GHG Emissions', 'S3-05', 'Waste Generated in Operations', 'S3-05-03', 'Incinerated Waste', 0.90751000, 'kg CO2e/kg', 'Waste incineration with energy recovery'),
(3, 'Other Indirect GHG Emissions', 'S3-05', 'Waste Generated in Operations', 'S3-05-04', 'Composted Organic Waste', 0.15400000, 'kg CO2e/kg', 'Organic waste composting'),
(3, 'Other Indirect GHG Emissions', 'S3-05', 'Waste Generated in Operations', 'S3-05-05', 'Hazardous Waste Treatment', 1.20000000, 'kg CO2e/kg', 'Hazardous waste treatment and disposal'),
(3, 'Other Indirect GHG Emissions', 'S3-05', 'Waste Generated in Operations', 'S3-05-06', 'Electronic Waste (WEEE)', 2.50000000, 'kg CO2e/kg', 'Electronic waste recycling'),

-- Category 6: Business Travel
(3, 'Other Indirect GHG Emissions', 'S3-06', 'Business Travel', 'S3-06-01', 'Air Travel Domestic (UK)', 0.24587000, 'kg CO2e/passenger.km', 'Domestic flights within UK'),
(3, 'Other Indirect GHG Emissions', 'S3-06', 'Business Travel', 'S3-06-02', 'Air Travel Short Haul (<3.7h)', 0.15845000, 'kg CO2e/passenger.km', 'Short haul international flights'),
(3, 'Other Indirect GHG Emissions', 'S3-06', 'Business Travel', 'S3-06-03', 'Air Travel Long Haul (>3.7h)', 0.19085000, 'kg CO2e/passenger.km', 'Long haul international flights'),
(3, 'Other Indirect GHG Emissions', 'S3-06', 'Business Travel', 'S3-06-04', 'Rail Travel (National)', 0.03549000, 'kg CO2e/passenger.km', 'Train travel within UK'),
(3, 'Other Indirect GHG Emissions', 'S3-06', 'Business Travel', 'S3-06-05', 'Taxi and Private Hire', 0.16743000, 'kg CO2e/passenger.km', 'Business taxi and private car hire'),
(3, 'Other Indirect GHG Emissions', 'S3-06', 'Business Travel', 'S3-06-06', 'Hotel Accommodation', 26.20000000, 'kg CO2e/room.night', 'Hotel stays for business travel'),
(3, 'Other Indirect GHG Emissions', 'S3-06', 'Business Travel', 'S3-06-07', 'Car Rental', 0.16743000, 'kg CO2e/km', 'Rental car usage for business'),

-- Category 7: Employee Commuting
(3, 'Other Indirect GHG Emissions', 'S3-07', 'Employee Commuting', 'S3-07-01', 'Car Commuting (Average)', 0.16743000, 'kg CO2e/passenger.km', 'Employee car commuting'),
(3, 'Other Indirect GHG Emissions', 'S3-07', 'Employee Commuting', 'S3-07-02', 'Bus Commuting', 0.10312000, 'kg CO2e/passenger.km', 'Bus commuting to work'),
(3, 'Other Indirect GHG Emissions', 'S3-07', 'Employee Commuting', 'S3-07-03', 'Rail Commuting', 0.03549000, 'kg CO2e/passenger.km', 'Train commuting to work'),
(3, 'Other Indirect GHG Emissions', 'S3-07', 'Employee Commuting', 'S3-07-04', 'Motorcycle Commuting', 0.11449000, 'kg CO2e/passenger.km', 'Motorcycle commuting to work'),
(3, 'Other Indirect GHG Emissions', 'S3-07', 'Employee Commuting', 'S3-07-05', 'Working from Home', 0.15200000, 'kg CO2e/day', 'Home office energy use and equipment'),
(3, 'Other Indirect GHG Emissions', 'S3-07', 'Employee Commuting', 'S3-07-06', 'Cycling (E-bike)', 0.00500000, 'kg CO2e/km', 'Electric bicycle commuting'),

-- Category 8: Upstream Leased Assets
(3, 'Other Indirect GHG Emissions', 'S3-08', 'Upstream Leased Assets', 'S3-08-01', 'Leased Office Buildings', 50.00000000, 'kg CO2e/m²/year', 'Leased office space energy use'),
(3, 'Other Indirect GHG Emissions', 'S3-08', 'Upstream Leased Assets', 'S3-08-02', 'Leased Vehicles', 3500.00000000, 'kg CO2e/vehicle/year', 'Leased company vehicles'),
(3, 'Other Indirect GHG Emissions', 'S3-08', 'Upstream Leased Assets', 'S3-08-03', 'Leased Equipment', 150.00000000, 'kg CO2e/unit/year', 'Leased machinery and equipment'),
(3, 'Other Indirect GHG Emissions', 'S3-08', 'Upstream Leased Assets', 'S3-08-04', 'Leased IT Equipment', 80.00000000, 'kg CO2e/unit/year', 'Leased computers and IT hardware'),

-- Category 9: Downstream Transportation and Distribution
(3, 'Other Indirect GHG Emissions', 'S3-09', 'Downstream Transportation and Distribution', 'S3-09-01', 'Product Distribution (Road)', 0.11449000, 'kg CO2e/tonne.km', 'Product delivery to customers by road'),
(3, 'Other Indirect GHG Emissions', 'S3-09', 'Downstream Transportation and Distribution', 'S3-09-02', 'Customer Collection', 0.16743000, 'kg CO2e/trip', 'Customer pickup journeys'),
(3, 'Other Indirect GHG Emissions', 'S3-09', 'Downstream Transportation and Distribution', 'S3-09-03', 'Retail/Warehouse Storage', 25.00000000, 'kg CO2e/m²/year', 'Retail and warehouse storage facilities'),
(3, 'Other Indirect GHG Emissions', 'S3-09', 'Downstream Transportation and Distribution', 'S3-09-04', 'Last Mile Delivery', 0.50000000, 'kg CO2e/delivery', 'Final delivery to end customer'),

-- Category 10: Processing of Sold Products
(3, 'Other Indirect GHG Emissions', 'S3-10', 'Processing of Sold Products', 'S3-10-01', 'Industrial Processing', 2.50000000, 'kg CO2e/kg', 'Customer processing of intermediate products'),
(3, 'Other Indirect GHG Emissions', 'S3-10', 'Processing of Sold Products', 'S3-10-02', 'Food Processing', 1.80000000, 'kg CO2e/kg', 'Food product processing by customers'),
(3, 'Other Indirect GHG Emissions', 'S3-10', 'Processing of Sold Products', 'S3-10-03', 'Chemical Processing', 3.20000000, 'kg CO2e/kg', 'Chemical processing of sold materials'),

-- Category 11: Use of Sold Products
(3, 'Other Indirect GHG Emissions', 'S3-11', 'Use of Sold Products', 'S3-11-01', 'Product Energy Use', 0.19338000, 'kg CO2e/kWh', 'Energy consumed during product use'),
(3, 'Other Indirect GHG Emissions', 'S3-11', 'Use of Sold Products', 'S3-11-02', 'Vehicle Fuel Use', 0.16743000, 'kg CO2e/litre', 'Fuel consumed by sold vehicles'),
(3, 'Other Indirect GHG Emissions', 'S3-11', 'Use of Sold Products', 'S3-11-03', 'Software/Digital Services', 0.00050000, 'kg CO2e/user.hour', 'Digital product usage emissions'),
(3, 'Other Indirect GHG Emissions', 'S3-11', 'Use of Sold Products', 'S3-11-04', 'Appliance Energy Use', 0.19338000, 'kg CO2e/kWh', 'Energy use of sold appliances'),

-- Category 12: End-of-life Treatment of Sold Products
(3, 'Other Indirect GHG Emissions', 'S3-12', 'End-of-life Treatment of Sold Products', 'S3-12-01', 'Product Disposal (Landfill)', 0.45751000, 'kg CO2e/kg', 'Product disposal at end of life'),
(3, 'Other Indirect GHG Emissions', 'S3-12', 'End-of-life Treatment of Sold Products', 'S3-12-02', 'Product Recycling', 0.02077000, 'kg CO2e/kg', 'Product recycling at end of life'),
(3, 'Other Indirect GHG Emissions', 'S3-12', 'End-of-life Treatment of Sold Products', 'S3-12-03', 'Product Incineration', 0.90751000, 'kg CO2e/kg', 'Product incineration at end of life'),
(3, 'Other Indirect GHG Emissions', 'S3-12', 'End-of-life Treatment of Sold Products', 'S3-12-04', 'Electronic Waste Treatment', 2.50000000, 'kg CO2e/kg', 'Electronic product end-of-life'),

-- Category 13: Downstream Leased Assets
(3, 'Other Indirect GHG Emissions', 'S3-13', 'Downstream Leased Assets', 'S3-13-01', 'Assets Leased to Customers', 50.00000000, 'kg CO2e/m²/year', 'Buildings and assets leased to customers'),
(3, 'Other Indirect GHG Emissions', 'S3-13', 'Downstream Leased Assets', 'S3-13-02', 'Franchisee Operations', 2500.00000000, 'kg CO2e/location/year', 'Franchisee energy use and operations'),
(3, 'Other Indirect GHG Emissions', 'S3-13', 'Downstream Leased Assets', 'S3-13-03', 'Equipment Leased to Customers', 200.00000000, 'kg CO2e/unit/year', 'Equipment leased to customers'),

-- Category 14: Franchises
(3, 'Other Indirect GHG Emissions', 'S3-14', 'Franchises', 'S3-14-01', 'Franchise Operations', 5000.00000000, 'kg CO2e/franchise/year', 'Franchise location operations and energy'),
(3, 'Other Indirect GHG Emissions', 'S3-14', 'Franchises', 'S3-14-02', 'Franchise Transport', 1200.00000000, 'kg CO2e/franchise/year', 'Franchise delivery and transport'),
(3, 'Other Indirect GHG Emissions', 'S3-14', 'Franchises', 'S3-14-03', 'Franchise Waste', 800.00000000, 'kg CO2e/franchise/year', 'Franchise waste generation'),

-- Category 15: Investments
(3, 'Other Indirect GHG Emissions', 'S3-15', 'Investments', 'S3-15-01', 'Equity Investments', 0.25000000, 'kg CO2e/£', 'Emissions from equity investments'),
(3, 'Other Indirect GHG Emissions', 'S3-15', 'Investments', 'S3-15-02', 'Debt Investments', 0.15000000, 'kg CO2e/£', 'Emissions from debt investments'),
(3, 'Other Indirect GHG Emissions', 'S3-15', 'Investments', 'S3-15-03', 'Project Finance', 0.35000000, 'kg CO2e/£', 'Project finance emissions'),
(3, 'Other Indirect GHG Emissions', 'S3-15', 'Investments', 'S3-15-04', 'Government Bonds', 0.08000000, 'kg CO2e/£', 'Government bond investments');
