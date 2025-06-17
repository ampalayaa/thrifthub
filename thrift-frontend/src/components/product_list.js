import React, { useEffect, useState } from 'react';
import { fetchProducts } from '../services/api';

const ProductList = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetchProducts().then(res => setProducts(res.data));
  }, []);

  return (
    <div>
      <h2>Available Products</h2>
      {products.map(p => (
        <div key={p.id}>
          <h4>{p.name}</h4>
          <p>{p.description}</p>
          <p>₱{p.price}</p>
        </div>
      ))}
    </div>
  );
};

export default ProductList;
