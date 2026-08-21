-- Day 16: Advanced Database Indexing & Query Optimization
-- Migration: add indexes for orders table performance

CREATE INDEX IF NOT EXISTS idx_orders_city ON orders(city);
CREATE INDEX IF NOT EXISTS idx_orders_pending ON orders(status) WHERE status = 'pending';
CREATE INDEX IF NOT EXISTS idx_city_status_amount ON orders(city, status, amount);
CREATE INDEX IF NOT EXISTS idx_covering_city_amount ON orders(city, amount);
CREATE INDEX IF NOT EXISTS idx_optimal_name_status_amount ON orders(customer_name, status, amount);