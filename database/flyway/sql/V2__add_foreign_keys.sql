ALTER TABLE product_category
    ADD CONSTRAINT fk_product_category_product
    FOREIGN KEY (product_id) REFERENCES product(id)
    ON DELETE CASCADE;

ALTER TABLE product_category
    ADD CONSTRAINT fk_product_category_category
    FOREIGN KEY (category_id) REFERENCES category(id)
    ON DELETE CASCADE;

ALTER TABLE deal
    ADD CONSTRAINT fk_deal_customer
    FOREIGN KEY (customer_id) REFERENCES customer(id)
    ON DELETE RESTRICT;

ALTER TABLE deal_item
    ADD CONSTRAINT fk_deal_item_deal
    FOREIGN KEY (deal_id) REFERENCES deal(id)
    ON DELETE CASCADE;

ALTER TABLE deal_item
    ADD CONSTRAINT fk_deal_item_product
    FOREIGN KEY (product_id) REFERENCES product(id)
    ON DELETE RESTRICT;

