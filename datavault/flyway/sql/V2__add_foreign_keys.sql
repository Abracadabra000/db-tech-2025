ALTER TABLE deal_fact
  ADD CONSTRAINT fk_deal_fact_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key) ON DELETE RESTRICT,
  ADD CONSTRAINT fk_deal_fact_date     FOREIGN KEY (date_key)     REFERENCES dim_date(date_key)        ON DELETE RESTRICT;

ALTER TABLE dim_product_category_link
  ADD CONSTRAINT fk_dim_product_category_link_product FOREIGN KEY (product_key) REFERENCES dim_product(product_key) ON DELETE RESTRICT,
  ADD CONSTRAINT fk_dim_product_category_link_product_category FOREIGN KEY (product_category_key) REFERENCES dim_product_category(product_category_key) ON DELETE RESTRICT;