CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(100),
    stock INT DEFAULT 0
);

INSERT INTO products (name, price, category, stock)
VALUES
('Samsung Galaxy S25', 59999.00, 'Mobile', 20),
('Dell Inspiron Laptop', 74999.00, 'Laptop', 10),
('Logitech Keyboard', 2499.00, 'Accessories', 50);
10. Frontend Dockerfile
File: frontend/Dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
