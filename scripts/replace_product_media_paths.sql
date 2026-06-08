START TRANSACTION;

UPDATE merchant_product
SET image = REPLACE(image, '/images/products/', '/media/product/')
WHERE image LIKE '/images/products/%';

UPDATE merchant_product
SET image = REPLACE(image, '/media/images/products/', '/media/product/')
WHERE image LIKE '/media/images/products/%';

UPDATE merchant_product
SET image = REPLACE(image, '/media/products/2026/05/', '/media/product/')
WHERE image LIKE '/media/products/2026/05/%';

UPDATE merchant_product
SET image = REPLACE(image, '/media/products/2026/06/', '/media/product/')
WHERE image LIKE '/media/products/2026/06/%';

UPDATE blindbox
SET cover = REPLACE(cover, '/images/products/', '/media/product/')
WHERE cover LIKE '/images/products/%';

UPDATE blindbox
SET cover = REPLACE(cover, '/media/images/products/', '/media/product/')
WHERE cover LIKE '/media/images/products/%';

UPDATE blindbox
SET cover = REPLACE(cover, '/media/products/2026/05/', '/media/product/')
WHERE cover LIKE '/media/products/2026/05/%';

UPDATE blindbox
SET cover = REPLACE(cover, '/media/products/2026/06/', '/media/product/')
WHERE cover LIKE '/media/products/2026/06/%';

UPDATE blindbox_prize
SET image = REPLACE(image, '/images/products/', '/media/product/')
WHERE image LIKE '/images/products/%';

UPDATE blindbox_prize
SET image = REPLACE(image, '/media/images/products/', '/media/product/')
WHERE image LIKE '/media/images/products/%';

UPDATE blindbox_prize
SET image = REPLACE(image, '/media/products/2026/05/', '/media/product/')
WHERE image LIKE '/media/products/2026/05/%';

UPDATE blindbox_prize
SET image = REPLACE(image, '/media/products/2026/06/', '/media/product/')
WHERE image LIKE '/media/products/2026/06/%';

UPDATE blindbox_draw_record
SET prize_image = REPLACE(prize_image, '/images/products/', '/media/product/')
WHERE prize_image LIKE '/images/products/%';

UPDATE blindbox_draw_record
SET prize_image = REPLACE(prize_image, '/media/images/products/', '/media/product/')
WHERE prize_image LIKE '/media/images/products/%';

UPDATE blindbox_draw_record
SET prize_image = REPLACE(prize_image, '/media/products/2026/05/', '/media/product/')
WHERE prize_image LIKE '/media/products/2026/05/%';

UPDATE blindbox_draw_record
SET prize_image = REPLACE(prize_image, '/media/products/2026/06/', '/media/product/')
WHERE prize_image LIKE '/media/products/2026/06/%';

UPDATE user_asset
SET product_image = REPLACE(product_image, '/images/products/', '/media/product/')
WHERE product_image LIKE '/images/products/%';

UPDATE user_asset
SET product_image = REPLACE(product_image, '/media/images/products/', '/media/product/')
WHERE product_image LIKE '/media/images/products/%';

UPDATE user_asset
SET product_image = REPLACE(product_image, '/media/products/2026/05/', '/media/product/')
WHERE product_image LIKE '/media/products/2026/05/%';

UPDATE user_asset
SET product_image = REPLACE(product_image, '/media/products/2026/06/', '/media/product/')
WHERE product_image LIKE '/media/products/2026/06/%';

UPDATE exchange_post
SET asset_image = REPLACE(asset_image, '/images/products/', '/media/product/')
WHERE asset_image LIKE '/images/products/%';

UPDATE exchange_post
SET asset_image = REPLACE(asset_image, '/media/images/products/', '/media/product/')
WHERE asset_image LIKE '/media/images/products/%';

UPDATE exchange_post
SET asset_image = REPLACE(asset_image, '/media/products/2026/05/', '/media/product/')
WHERE asset_image LIKE '/media/products/2026/05/%';

UPDATE exchange_post
SET asset_image = REPLACE(asset_image, '/media/products/2026/06/', '/media/product/')
WHERE asset_image LIKE '/media/products/2026/06/%';

UPDATE exchange_application
SET applicant_asset_image = REPLACE(applicant_asset_image, '/images/products/', '/media/product/')
WHERE applicant_asset_image LIKE '/images/products/%';

UPDATE exchange_application
SET applicant_asset_image = REPLACE(applicant_asset_image, '/media/images/products/', '/media/product/')
WHERE applicant_asset_image LIKE '/media/images/products/%';

UPDATE exchange_application
SET applicant_asset_image = REPLACE(applicant_asset_image, '/media/products/2026/05/', '/media/product/')
WHERE applicant_asset_image LIKE '/media/products/2026/05/%';

UPDATE exchange_application
SET applicant_asset_image = REPLACE(applicant_asset_image, '/media/products/2026/06/', '/media/product/')
WHERE applicant_asset_image LIKE '/media/products/2026/06/%';

UPDATE exchange_application
SET post_asset_image = REPLACE(post_asset_image, '/images/products/', '/media/product/')
WHERE post_asset_image LIKE '/images/products/%';

UPDATE exchange_application
SET post_asset_image = REPLACE(post_asset_image, '/media/images/products/', '/media/product/')
WHERE post_asset_image LIKE '/media/images/products/%';

UPDATE exchange_application
SET post_asset_image = REPLACE(post_asset_image, '/media/products/2026/05/', '/media/product/')
WHERE post_asset_image LIKE '/media/products/2026/05/%';

UPDATE exchange_application
SET post_asset_image = REPLACE(post_asset_image, '/media/products/2026/06/', '/media/product/')
WHERE post_asset_image LIKE '/media/products/2026/06/%';

UPDATE `order`
SET asset_image = REPLACE(asset_image, '/images/products/', '/media/product/')
WHERE asset_image LIKE '/images/products/%';

UPDATE `order`
SET asset_image = REPLACE(asset_image, '/media/images/products/', '/media/product/')
WHERE asset_image LIKE '/media/images/products/%';

UPDATE `order`
SET asset_image = REPLACE(asset_image, '/media/products/2026/05/', '/media/product/')
WHERE asset_image LIKE '/media/products/2026/05/%';

UPDATE `order`
SET asset_image = REPLACE(asset_image, '/media/products/2026/06/', '/media/product/')
WHERE asset_image LIKE '/media/products/2026/06/%';

COMMIT;
