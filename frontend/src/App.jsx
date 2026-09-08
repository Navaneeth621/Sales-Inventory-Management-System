import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [activePage, setActivePage] = useState("Dashboard");

  const [products, setProducts] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [sales, setSales] = useState([]);
  const [salesReport, setSalesReport] = useState(null);
  const [lowStockProducts, setLowStockProducts] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // ============================================================
  // PRODUCT STATES
  // ============================================================

  const [productSearch, setProductSearch] = useState("");
  const [showProductForm, setShowProductForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [productMessage, setProductMessage] = useState("");
  const [productError, setProductError] = useState("");

  const emptyProduct = {
    product_id: "",
    name: "",
    category: "",
    price: "",
    quantity: "",
  };

  const [productForm, setProductForm] = useState(emptyProduct);

  // ============================================================
  // CUSTOMER STATES
  // ============================================================

  const [customerSearch, setCustomerSearch] = useState("");
  const [showCustomerForm, setShowCustomerForm] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState(null);
  const [customerMessage, setCustomerMessage] = useState("");
  const [customerError, setCustomerError] = useState("");

  const emptyCustomer = {
    customer_id: "",
    name: "",
    phone: "",
  };

  const [customerForm, setCustomerForm] = useState(emptyCustomer);

  // ============================================================
  // SALES STATES
  // ============================================================

  const [showSaleForm, setShowSaleForm] = useState(false);
  const [saleMessage, setSaleMessage] = useState("");
  const [saleError, setSaleError] = useState("");
  const [saleSearch, setSaleSearch] = useState("");

  const emptySale = {
    customer_id: "",
    product_id: "",
    quantity: "",
  };

  const [saleForm, setSaleForm] = useState(emptySale);

  // ============================================================
  // INITIAL DATA
  // ============================================================

  useEffect(() => {
    fetchDashboardData();
  }, []);

  async function fetchDashboardData() {
    try {
      setLoading(true);
      setError("");

      const [
        productsResponse,
        customersResponse,
        salesResponse,
        salesReportResponse,
        lowStockResponse,
      ] = await Promise.all([
        fetch(`${API_URL}/products`),
        fetch(`${API_URL}/customers`),
        fetch(`${API_URL}/sales`),
        fetch(`${API_URL}/reports/sales`),
        fetch(`${API_URL}/reports/low-stock`),
      ]);

      if (
        !productsResponse.ok ||
        !customersResponse.ok ||
        !salesResponse.ok ||
        !salesReportResponse.ok ||
        !lowStockResponse.ok
      ) {
        throw new Error("Failed to fetch dashboard data");
      }

      const productsData = await productsResponse.json();
      const customersData = await customersResponse.json();
      const salesData = await salesResponse.json();
      const salesReportData = await salesReportResponse.json();
      const lowStockData = await lowStockResponse.json();

      setProducts(productsData);
      setCustomers(customersData);
      setSales(salesData);
      setSalesReport(salesReportData);

      setLowStockProducts(
        Array.isArray(lowStockData)
          ? lowStockData
          : lowStockData.products || []
      );
    } catch (err) {
      console.error("Dashboard error:", err);

      setError(
        "Unable to connect to the backend. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  }

  // ============================================================
  // NAVIGATION
  // ============================================================

  const menuItems = [
    { name: "Dashboard", icon: "▦" },
    { name: "Products", icon: "📦" },
    { name: "Customers", icon: "👥" },
    { name: "Sales", icon: "🛒" },
    { name: "Reports", icon: "📊" },
  ];

  // ============================================================
  // HELPERS
  // ============================================================

  const totalProducts = products.length;
  const totalCustomers = customers.length;

  const totalSales =
    salesReport?.total_transactions ?? sales.length;

  const totalRevenue = salesReport?.total_revenue ?? 0;

  const recentSales = [...sales]
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 4);

  function formatCurrency(value) {
    return `₹${Number(value || 0).toLocaleString("en-IN", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    })}`;
  }

  function getCustomerName(customerId) {
    const customer = customers.find(
      (item) => item.customer_id === customerId
    );

    return customer ? customer.name : customerId;
  }

  function getProductName(productId) {
    const product = products.find(
      (item) => item.product_id === productId
    );

    return product ? product.name : productId;
  }

  // ============================================================
  // REPORT CHART DATA
  // ============================================================

  /*
    Revenue trend:
    Group all sales by date and calculate the total revenue
    generated on each date.
  */

  const revenueByDate = {};

  sales.forEach((sale) => {
    if (!sale.date) {
      return;
    }

    const parsedDate = new Date(sale.date);

    if (Number.isNaN(parsedDate.getTime())) {
      return;
    }

    const dateKey = parsedDate.toISOString().split("T")[0];

    if (!revenueByDate[dateKey]) {
      revenueByDate[dateKey] = 0;
    }

    revenueByDate[dateKey] += Number(sale.total || 0);
  });

  const revenueTrendData = Object.entries(revenueByDate)
    .sort(([dateA], [dateB]) =>
      dateA.localeCompare(dateB)
    )
    .map(([date, revenue]) => {
      const displayDate = new Date(`${date}T00:00:00`);

      return {
        date: displayDate.toLocaleDateString("en-IN", {
          day: "2-digit",
          month: "short",
        }),
        revenue: Number(revenue.toFixed(2)),
      };
    });

  const stockChartData = [
    {
      name: "Low Stock",
      value: lowStockProducts.length,
    },
    {
      name: "Healthy Stock",
      value: Math.max(
        products.length - lowStockProducts.length,
        0
      ),
    },
  ];

  // ============================================================
  // PRODUCT PAGE
  // ============================================================

  const filteredProducts = products.filter((product) => {
    const search = productSearch.toLowerCase().trim();

    if (!search) {
      return true;
    }

    return (
      product.product_id.toLowerCase().includes(search) ||
      product.name.toLowerCase().includes(search) ||
      product.category.toLowerCase().includes(search)
    );
  });

  function openAddProduct() {
    setEditingProduct(null);
    setProductForm(emptyProduct);
    setProductMessage("");
    setProductError("");
    setShowProductForm(true);
  }

  function openEditProduct(product) {
    setEditingProduct(product);

    setProductForm({
      product_id: product.product_id,
      name: product.name,
      category: product.category,
      price: product.price,
      quantity: product.quantity,
    });

    setProductMessage("");
    setProductError("");
    setShowProductForm(true);
  }

  function closeProductForm() {
    setShowProductForm(false);
    setEditingProduct(null);
    setProductForm(emptyProduct);
    setProductMessage("");
    setProductError("");
  }

  function handleProductInput(event) {
    const { name, value } = event.target;

    setProductForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handleProductSubmit(event) {
    event.preventDefault();

    setProductMessage("");
    setProductError("");

    if (!productForm.product_id.trim()) {
      setProductError("Product ID is required.");
      return;
    }

    if (!productForm.name.trim()) {
      setProductError("Product name is required.");
      return;
    }

    if (!productForm.category.trim()) {
      setProductError("Category is required.");
      return;
    }

    const price = Number(productForm.price);
    const quantity = Number(productForm.quantity);

    if (!Number.isFinite(price) || price <= 0) {
      setProductError("Price must be greater than zero.");
      return;
    }

    if (!Number.isInteger(quantity) || quantity < 0) {
      setProductError("Quantity must be zero or greater.");
      return;
    }

    try {
      const isEditing = Boolean(editingProduct);

      const url = isEditing
        ? `${API_URL}/products/${editingProduct.product_id}`
        : `${API_URL}/products`;

      const method = isEditing ? "PUT" : "POST";

      const body = isEditing
        ? {
            name: productForm.name.trim(),
            category: productForm.category.trim(),
            price,
            quantity,
          }
        : {
            product_id: productForm.product_id.trim(),
            name: productForm.name.trim(),
            category: productForm.category.trim(),
            price,
            quantity,
          };

      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to save product."
        );
      }

      setProductMessage(
        isEditing
          ? "Product updated successfully."
          : "Product added successfully."
      );

      await fetchDashboardData();

      setTimeout(() => {
        closeProductForm();
      }, 700);
    } catch (err) {
      console.error("Product save error:", err);
      setProductError(err.message);
    }
  }

  async function handleDeleteProduct(productId) {
    const confirmed = window.confirm(
      `Are you sure you want to delete product ${productId}?`
    );

    if (!confirmed) {
      return;
    }

    setProductMessage("");
    setProductError("");

    try {
      const response = await fetch(
        `${API_URL}/products/${productId}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to delete product."
        );
      }

      setProductMessage("Product deleted successfully.");

      await fetchDashboardData();
    } catch (err) {
      console.error("Product delete error:", err);
      setProductError(err.message);
    }
  }

  // ============================================================
  // CUSTOMER PAGE
  // ============================================================

  const filteredCustomers = customers.filter((customer) => {
    const search = customerSearch.toLowerCase().trim();

    if (!search) {
      return true;
    }

    return (
      customer.customer_id.toLowerCase().includes(search) ||
      customer.name.toLowerCase().includes(search) ||
      customer.phone.toLowerCase().includes(search)
    );
  });

  function openAddCustomer() {
    setEditingCustomer(null);
    setCustomerForm(emptyCustomer);
    setCustomerMessage("");
    setCustomerError("");
    setShowCustomerForm(true);
  }

  function openEditCustomer(customer) {
    setEditingCustomer(customer);

    setCustomerForm({
      customer_id: customer.customer_id,
      name: customer.name,
      phone: customer.phone,
    });

    setCustomerMessage("");
    setCustomerError("");
    setShowCustomerForm(true);
  }

  function closeCustomerForm() {
    setShowCustomerForm(false);
    setEditingCustomer(null);
    setCustomerForm(emptyCustomer);
    setCustomerMessage("");
    setCustomerError("");
  }

  function handleCustomerInput(event) {
    const { name, value } = event.target;

    setCustomerForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handleCustomerSubmit(event) {
    event.preventDefault();

    setCustomerMessage("");
    setCustomerError("");

    if (!customerForm.customer_id.trim()) {
      setCustomerError("Customer ID is required.");
      return;
    }

    if (!customerForm.name.trim()) {
      setCustomerError("Customer name is required.");
      return;
    }

    const phone = customerForm.phone.trim();

    if (!/^\d{10}$/.test(phone)) {
      setCustomerError(
        "Phone number must be exactly 10 digits."
      );
      return;
    }

    try {
      const isEditing = Boolean(editingCustomer);

      const url = isEditing
        ? `${API_URL}/customers/${editingCustomer.customer_id}`
        : `${API_URL}/customers`;

      const method = isEditing ? "PUT" : "POST";

      const body = isEditing
        ? {
            name: customerForm.name.trim(),
            phone,
          }
        : {
            customer_id: customerForm.customer_id.trim(),
            name: customerForm.name.trim(),
            phone,
          };

      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to save customer."
        );
      }

      setCustomerMessage(
        isEditing
          ? "Customer updated successfully."
          : "Customer added successfully."
      );

      await fetchDashboardData();

      setTimeout(() => {
        closeCustomerForm();
      }, 700);
    } catch (err) {
      console.error("Customer save error:", err);
      setCustomerError(err.message);
    }
  }

  async function handleDeleteCustomer(customerId) {
    const confirmed = window.confirm(
      `Are you sure you want to delete customer ${customerId}?`
    );

    if (!confirmed) {
      return;
    }

    setCustomerMessage("");
    setCustomerError("");

    try {
      const response = await fetch(
        `${API_URL}/customers/${customerId}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to delete customer."
        );
      }

      setCustomerMessage(
        "Customer deleted successfully."
      );

      await fetchDashboardData();
    } catch (err) {
      console.error("Customer delete error:", err);
      setCustomerError(err.message);
    }
  }

  // ============================================================
  // SALES PAGE
  // ============================================================

  const filteredSales = sales.filter((sale) => {
    const search = saleSearch.toLowerCase().trim();

    if (!search) {
      return true;
    }

    return (
      sale.sale_id.toLowerCase().includes(search) ||
      sale.customer_id.toLowerCase().includes(search) ||
      sale.product_id.toLowerCase().includes(search) ||
      getCustomerName(sale.customer_id)
        .toLowerCase()
        .includes(search) ||
      getProductName(sale.product_id)
        .toLowerCase()
        .includes(search)
    );
  });

  function openAddSale() {
    setSaleForm({
      customer_id:
        customers.length > 0
          ? customers[0].customer_id
          : "",
      product_id:
        products.length > 0
          ? products.find((p) => p.quantity > 0)?.product_id ||
            products[0].product_id
          : "",
      quantity: "",
    });

    setSaleMessage("");
    setSaleError("");
    setShowSaleForm(true);
  }

  function closeSaleForm() {
    setShowSaleForm(false);
    setSaleForm(emptySale);
    setSaleMessage("");
    setSaleError("");
  }

  function handleSaleInput(event) {
    const { name, value } = event.target;

    setSaleForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  const selectedSaleProduct = products.find(
    (product) =>
      product.product_id === saleForm.product_id
  );

  const saleQuantity = Number(saleForm.quantity || 0);

  const saleEstimatedTotal =
    selectedSaleProduct && saleQuantity > 0
      ? Number(selectedSaleProduct.price) * saleQuantity
      : 0;

  async function handleSaleSubmit(event) {
    event.preventDefault();

    setSaleMessage("");
    setSaleError("");

    if (!saleForm.customer_id) {
      setSaleError("Please select a customer.");
      return;
    }

    if (!saleForm.product_id) {
      setSaleError("Please select a product.");
      return;
    }

    const quantity = Number(saleForm.quantity);

    if (!Number.isInteger(quantity) || quantity <= 0) {
      setSaleError(
        "Quantity must be a whole number greater than zero."
      );
      return;
    }

    if (
      selectedSaleProduct &&
      quantity > selectedSaleProduct.quantity
    ) {
      setSaleError(
        `Only ${selectedSaleProduct.quantity} units are available in stock.`
      );
      return;
    }

    try {
      const response = await fetch(`${API_URL}/sales`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          customer_id: saleForm.customer_id,
          product_id: saleForm.product_id,
          quantity,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to record sale."
        );
      }

      setSaleMessage("Sale recorded successfully.");

      await fetchDashboardData();

      setTimeout(() => {
        closeSaleForm();
      }, 800);
    } catch (err) {
      console.error("Sale error:", err);
      setSaleError(err.message);
    }
  }

  // ============================================================
  // STAT CARDS
  // ============================================================

  const stats = [
    {
      title: "Total Products",
      value: loading ? "..." : totalProducts,
      subtitle: "Products in inventory",
      icon: "📦",
    },
    {
      title: "Total Customers",
      value: loading ? "..." : totalCustomers,
      subtitle: "Registered customers",
      icon: "👥",
    },
    {
      title: "Total Sales",
      value: loading ? "..." : totalSales,
      subtitle: "Completed transactions",
      icon: "🛒",
    },
    {
      title: "Total Revenue",
      value: loading ? "..." : formatCurrency(totalRevenue),
      subtitle: "Overall sales revenue",
      icon: "₹",
    },
  ];

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className="app">

      {/* ========================================================
          SIDEBAR
      ======================================================== */}

      <aside className="sidebar">

        <div className="logo-section">
          <div className="logo-icon">S</div>

          <div>
            <h2>Smart Sales</h2>
            <p>Inventory Management</p>
          </div>
        </div>

        <nav className="navigation">

          <p className="menu-title">MAIN MENU</p>

          {menuItems.map((item) => (
            <button
              key={item.name}
              className={`nav-item ${
                activePage === item.name ? "active" : ""
              }`}
              onClick={() => setActivePage(item.name)}
            >
              <span className="nav-icon">
                {item.icon}
              </span>

              <span>{item.name}</span>
            </button>
          ))}

        </nav>

        <div className="sidebar-bottom">

          <div className="system-status">

            <span
              className={`status-dot ${
                error ? "offline" : ""
              }`}
            ></span>

            <div>
              <strong>
                {error
                  ? "Backend Offline"
                  : "System Online"}
              </strong>

              <small>
                {error
                  ? "FastAPI connection failed"
                  : "MySQL Database Connected"}
              </small>
            </div>

          </div>

        </div>

      </aside>

      {/* ========================================================
          MAIN CONTENT
      ======================================================== */}

      <main className="main-content">

        <header className="top-header">

          <div>
            <h1>{activePage}</h1>

            <p>
              Welcome back! Here's what's happening
              with your business today.
            </p>
          </div>

          <div className="header-right">

            <div className="date-box">
              <span>📅</span>
              <span>August 2026</span>
            </div>

            <div className="profile">

              <div className="profile-avatar">
                N
              </div>

              <div>
                <strong>Admin</strong>
                <small>Administrator</small>
              </div>

            </div>

          </div>

        </header>

        {/* ======================================================
            GLOBAL ERROR
        ====================================================== */}

        {error && activePage !== "Dashboard" && (
          <div style={errorBoxStyle}>
            {error}
          </div>
        )}

        {/* ======================================================
            DASHBOARD
        ====================================================== */}

        {activePage === "Dashboard" && (
          <>

            {error && (
              <div style={errorBoxStyle}>
                {error}
              </div>
            )}

            <section className="stats-grid">

              {stats.map((stat) => (

                <div
                  className="stat-card"
                  key={stat.title}
                >

                  <div className="stat-top">

                    <div>
                      <p>{stat.title}</p>
                      <h2>{stat.value}</h2>
                    </div>

                    <div className="stat-icon">
                      {stat.icon}
                    </div>

                  </div>

                  <span className="stat-subtitle">
                    {stat.subtitle}
                  </span>

                </div>

              ))}

            </section>

            <section className="dashboard-grid">

              {/* RECENT SALES */}

              <div className="dashboard-card sales-card">

                <div className="card-header">

                  <div>
                    <h3>Recent Sales</h3>
                    <p>Latest transactions</p>
                  </div>

                  <button
                    className="view-button"
                    onClick={() =>
                      setActivePage("Sales")
                    }
                  >
                    View All
                  </button>

                </div>

                <div className="table-container">

                  {loading ? (

                    <div style={emptyStateStyle}>
                      Loading sales...
                    </div>

                  ) : recentSales.length === 0 ? (

                    <div style={emptyStateStyle}>
                      No sales found.
                    </div>

                  ) : (

                    <table>

                      <thead>
                        <tr>
                          <th>Sale ID</th>
                          <th>Customer</th>
                          <th>Product</th>
                          <th>Qty</th>
                          <th>Total</th>
                        </tr>
                      </thead>

                      <tbody>

                        {recentSales.map((sale) => (

                          <tr key={sale.sale_id}>

                            <td>
                              <span className="sale-id">
                                {sale.sale_id}
                              </span>
                            </td>

                            <td>
                              {getCustomerName(
                                sale.customer_id
                              )}
                            </td>

                            <td>
                              {getProductName(
                                sale.product_id
                              )}
                            </td>

                            <td>
                              {sale.quantity}
                            </td>

                            <td>
                              <strong>
                                {formatCurrency(
                                  sale.total
                                )}
                              </strong>
                            </td>

                          </tr>

                        ))}

                      </tbody>

                    </table>

                  )}

                </div>

              </div>

              {/* LOW STOCK */}

              <div className="dashboard-card stock-card">

                <div className="card-header">

                  <div>
                    <h3>Low Stock Alert</h3>

                    <p>
                      Products requiring attention
                    </p>
                  </div>

                  <button
                    className="alert-count"
                    onClick={() =>
                      setActivePage("Products")
                    }
                  >
                    {lowStockProducts.length}
                  </button>

                </div>

                <div className="stock-list">

                  {loading ? (

                    <div style={emptyStateStyle}>
                      Loading...
                    </div>

                  ) : lowStockProducts.length === 0 ? (

                    <div style={emptyStateStyle}>
                      No low-stock products.
                    </div>

                  ) : (

                    lowStockProducts.map((product) => (

                      <div
                        className="stock-item"
                        key={product.product_id}
                      >

                        <div className="product-icon">
                          📦
                        </div>

                        <div className="product-info">

                          <strong>
                            {product.name}
                          </strong>

                          <span>
                            {product.product_id} ·{" "}
                            {product.category}
                          </span>

                        </div>

                        <div
                          className={`stock-number ${
                            product.quantity === 0
                              ? "out"
                              : ""
                          }`}
                        >
                          {product.quantity === 0
                            ? "Out of stock"
                            : `${product.quantity} left`}
                        </div>

                      </div>

                    ))

                  )}

                </div>

              </div>

            </section>

            <section className="quick-section">

              <div className="section-title">
                <h3>Quick Actions</h3>
                <p>Frequently used operations</p>
              </div>

              <div className="quick-grid">

                <button
                  className="quick-card"
                  onClick={() =>
                    setActivePage("Products")
                  }
                >
                  <div className="quick-icon blue">
                    📦
                  </div>

                  <div>
                    <strong>Manage Products</strong>
                    <span>
                      Add, update or delete products
                    </span>
                  </div>

                  <span className="arrow">→</span>
                </button>

                <button
                  className="quick-card"
                  onClick={() =>
                    setActivePage("Customers")
                  }
                >
                  <div className="quick-icon purple">
                    👥
                  </div>

                  <div>
                    <strong>Manage Customers</strong>
                    <span>
                      View and manage customers
                    </span>
                  </div>

                  <span className="arrow">→</span>
                </button>

                <button
                  className="quick-card"
                  onClick={() =>
                    setActivePage("Sales")
                  }
                >
                  <div className="quick-icon green">
                    🛒
                  </div>

                  <div>
                    <strong>Create Sale</strong>
                    <span>
                      Record a new transaction
                    </span>
                  </div>

                  <span className="arrow">→</span>
                </button>

                <button
                  className="quick-card"
                  onClick={() =>
                    setActivePage("Reports")
                  }
                >
                  <div className="quick-icon orange">
                    📊
                  </div>

                  <div>
                    <strong>View Reports</strong>
                    <span>
                      Analyze sales and inventory
                    </span>
                  </div>

                  <span className="arrow">→</span>
                </button>

              </div>

            </section>

          </>
        )}

        {/* ======================================================
            PRODUCTS PAGE
        ====================================================== */}

        {activePage === "Products" && (

          <section>

            <div className="page-header-row">

              <div>
                <h2 className="page-section-title">
                  Products
                </h2>

                <p className="page-section-subtitle">
                  Manage your inventory products
                </p>
              </div>

              <button
                onClick={openAddProduct}
                className="primary-button"
              >
                + Add Product
              </button>

            </div>

            {productMessage && (
              <div style={successBoxStyle}>
                {productMessage}
              </div>
            )}

            {productError && (
              <div style={errorBoxStyle}>
                {productError}
              </div>
            )}

            <div className="search-box">

              <input
                type="text"
                placeholder="Search by product ID, name or category..."
                value={productSearch}
                onChange={(e) =>
                  setProductSearch(e.target.value)
                }
              />

            </div>

            <div className="data-card">

              <div className="data-card-header">

                <strong>
                  Product Inventory
                </strong>

                <span>
                  {filteredProducts.length} products
                </span>

              </div>

              {loading ? (

                <div style={emptyStateStyle}>
                  Loading products...
                </div>

              ) : filteredProducts.length === 0 ? (

                <div style={emptyStateStyle}>
                  No products found.
                </div>

              ) : (

                <div className="table-scroll">

                  <table className="management-table">

                    <thead>
                      <tr>
                        <th>Product ID</th>
                        <th>Product</th>
                        <th>Category</th>
                        <th>Price</th>
                        <th>Stock</th>
                        <th>Status</th>
                        <th>Actions</th>
                      </tr>
                    </thead>

                    <tbody>

                      {filteredProducts.map(
                        (product) => (

                          <tr key={product.product_id}>

                            <td>
                              <strong className="blue-id">
                                {product.product_id}
                              </strong>
                            </td>

                            <td>

                              <div className="name-cell">

                                <div className="product-avatar">
                                  📦
                                </div>

                                <strong>
                                  {product.name}
                                </strong>

                              </div>

                            </td>

                            <td>
                              {product.category}
                            </td>

                            <td>
                              <strong>
                                {formatCurrency(
                                  product.price
                                )}
                              </strong>
                            </td>

                            <td>
                              <strong>
                                {product.quantity}
                              </strong>
                            </td>

                            <td>

                              {product.quantity === 0 ? (

                                <span className="status-danger">
                                  Out of Stock
                                </span>

                              ) : product.quantity <= 5 ? (

                                <span className="status-warning">
                                  Low Stock
                                </span>

                              ) : (

                                <span className="status-success">
                                  In Stock
                                </span>

                              )}

                            </td>

                            <td>

                              <div className="action-buttons">

                                <button
                                  onClick={() =>
                                    openEditProduct(product)
                                  }
                                  className="edit-button"
                                >
                                  Edit
                                </button>

                                <button
                                  onClick={() =>
                                    handleDeleteProduct(
                                      product.product_id
                                    )
                                  }
                                  className="delete-button"
                                >
                                  Delete
                                </button>

                              </div>

                            </td>

                          </tr>

                        )
                      )}

                    </tbody>

                  </table>

                </div>

              )}

            </div>

          </section>

        )}

        {/* ======================================================
            CUSTOMERS PAGE
        ====================================================== */}

        {activePage === "Customers" && (

          <section>

            <div className="page-header-row">

              <div>
                <h2 className="page-section-title">
                  Customers
                </h2>

                <p className="page-section-subtitle">
                  Manage your registered customers
                </p>
              </div>

              <button
                onClick={openAddCustomer}
                className="customer-primary-button"
              >
                + Add Customer
              </button>

            </div>

            {customerMessage && (
              <div style={successBoxStyle}>
                {customerMessage}
              </div>
            )}

            {customerError && (
              <div style={errorBoxStyle}>
                {customerError}
              </div>
            )}

            <div className="search-box">

              <input
                type="text"
                placeholder="Search by customer ID, name or phone..."
                value={customerSearch}
                onChange={(e) =>
                  setCustomerSearch(e.target.value)
                }
              />

            </div>

            <div className="data-card">

              <div className="data-card-header">

                <strong>
                  Customer Directory
                </strong>

                <span>
                  {filteredCustomers.length} customers
                </span>

              </div>

              {loading ? (

                <div style={emptyStateStyle}>
                  Loading customers...
                </div>

              ) : filteredCustomers.length === 0 ? (

                <div style={emptyStateStyle}>
                  No customers found.
                </div>

              ) : (

                <div className="table-scroll">

                  <table className="management-table">

                    <thead>
                      <tr>
                        <th>Customer ID</th>
                        <th>Customer</th>
                        <th>Phone</th>
                        <th>Status</th>
                        <th>Actions</th>
                      </tr>
                    </thead>

                    <tbody>

                      {filteredCustomers.map(
                        (customer) => (

                          <tr
                            key={customer.customer_id}
                          >

                            <td>
                              <strong className="purple-id">
                                {customer.customer_id}
                              </strong>
                            </td>

                            <td>

                              <div className="name-cell">

                                <div className="customer-avatar">
                                  {customer.name
                                    .charAt(0)
                                    .toUpperCase()}
                                </div>

                                <strong>
                                  {customer.name}
                                </strong>

                              </div>

                            </td>

                            <td>
                              {customer.phone}
                            </td>

                            <td>
                              <span className="status-success">
                                Active
                              </span>
                            </td>

                            <td>

                              <div className="action-buttons">

                                <button
                                  onClick={() =>
                                    openEditCustomer(
                                      customer
                                    )
                                  }
                                  className="edit-customer-button"
                                >
                                  Edit
                                </button>

                                <button
                                  onClick={() =>
                                    handleDeleteCustomer(
                                      customer.customer_id
                                    )
                                  }
                                  className="delete-button"
                                >
                                  Delete
                                </button>

                              </div>

                            </td>

                          </tr>

                        )
                      )}

                    </tbody>

                  </table>

                </div>

              )}

            </div>

          </section>

        )}

        {/* ======================================================
            SALES PAGE
        ====================================================== */}

        {activePage === "Sales" && (

          <section>

            <div className="page-header-row">

              <div>
                <h2 className="page-section-title">
                  Sales
                </h2>

                <p className="page-section-subtitle">
                  Record and manage sales transactions
                </p>
              </div>

              <button
                onClick={openAddSale}
                className="sale-primary-button"
              >
                + Create Sale
              </button>

            </div>

            {saleMessage && (
              <div style={successBoxStyle}>
                {saleMessage}
              </div>
            )}

            {saleError && !showSaleForm && (
              <div style={errorBoxStyle}>
                {saleError}
              </div>
            )}

            <div className="search-box">

              <input
                type="text"
                placeholder="Search by sale ID, customer or product..."
                value={saleSearch}
                onChange={(e) =>
                  setSaleSearch(e.target.value)
                }
              />

            </div>

            <div className="data-card">

              <div className="data-card-header">

                <strong>
                  Sales Transactions
                </strong>

                <span>
                  {filteredSales.length} transactions
                </span>

              </div>

              {loading ? (

                <div style={emptyStateStyle}>
                  Loading sales...
                </div>

              ) : filteredSales.length === 0 ? (

                <div style={emptyStateStyle}>
                  No sales found.
                </div>

              ) : (

                <div className="table-scroll">

                  <table className="management-table">

                    <thead>

                      <tr>
                        <th>Sale ID</th>
                        <th>Customer</th>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Total</th>
                        <th>Date</th>
                      </tr>

                    </thead>

                    <tbody>

                      {filteredSales.map((sale) => (

                        <tr key={sale.sale_id}>

                          <td>
                            <strong className="green-id">
                              {sale.sale_id}
                            </strong>
                          </td>

                          <td>

                            <div>
                              <strong>
                                {getCustomerName(
                                  sale.customer_id
                                )}
                              </strong>

                              <small className="table-subtext">
                                {sale.customer_id}
                              </small>
                            </div>

                          </td>

                          <td>

                            <div>
                              <strong>
                                {getProductName(
                                  sale.product_id
                                )}
                              </strong>

                              <small className="table-subtext">
                                {sale.product_id}
                              </small>
                            </div>

                          </td>

                          <td>
                            {sale.quantity}
                          </td>

                          <td>
                            <strong>
                              {formatCurrency(
                                sale.total
                              )}
                            </strong>
                          </td>

                          <td>
                            {sale.date
                              ? new Date(
                                  sale.date
                                ).toLocaleString(
                                  "en-IN"
                                )
                              : "-"}
                          </td>

                        </tr>

                      ))}

                    </tbody>

                  </table>

                </div>

              )}

            </div>

          </section>

        )}

        {/* ======================================================
            REPORTS PAGE
        ====================================================== */}

        {activePage === "Reports" && (

          <section className="reports-page">

            <div className="page-header-row">

              <div>
                <h2 className="page-section-title">
                  Reports
                </h2>

                <p className="page-section-subtitle">
                  Sales and inventory overview
                </p>
              </div>

              <button
                onClick={fetchDashboardData}
                className="primary-button"
              >
                ↻ Refresh
              </button>

            </div>

            {/* REPORT SUMMARY */}

            <div className="stats-grid reports-summary">

              <div className="stat-card">

                <div className="stat-top">

                  <div>
                    <p>Total Transactions</p>

                    <h2>
                      {salesReport?.total_transactions ?? 0}
                    </h2>
                  </div>

                  <div className="stat-icon">
                    🛒
                  </div>

                </div>

                <span className="stat-subtitle">
                  Completed sales
                </span>

              </div>

              <div className="stat-card">

                <div className="stat-top">

                  <div>
                    <p>Total Revenue</p>

                    <h2>
                      {formatCurrency(
                        salesReport?.total_revenue
                      )}
                    </h2>
                  </div>

                  <div className="stat-icon">
                    ₹
                  </div>

                </div>

                <span className="stat-subtitle">
                  Overall sales revenue
                </span>

              </div>

              <div className="stat-card">

                <div className="stat-top">

                  <div>
                    <p>Average Sale</p>

                    <h2>
                      {formatCurrency(
                        salesReport?.average_sale
                      )}
                    </h2>
                  </div>

                  <div className="stat-icon">
                    📈
                  </div>

                </div>

                <span className="stat-subtitle">
                  Average transaction value
                </span>

              </div>

              <div className="stat-card">

                <div className="stat-top">

                  <div>
                    <p>Low Stock Items</p>

                    <h2>
                      {lowStockProducts.length}
                    </h2>
                  </div>

                  <div className="stat-icon">
                    ⚠️
                  </div>

                </div>

                <span className="stat-subtitle">
                  Products requiring attention
                </span>

              </div>

            </div>

            {/* ==================================================
                CHARTS
            ================================================== */}

            <div
              className="dashboard-grid"
              style={{
                marginTop: "24px",
                marginBottom: "24px",
              }}
            >

              {/* REVENUE TREND */}

              <div className="data-card">

                <div className="data-card-header">

                  <div>
                    <strong>
                      Revenue Trend
                    </strong>

                    <div
                      style={{
                        fontSize: "12px",
                        color: "#9ca3af",
                        marginTop: "4px",
                      }}
                    >
                      Revenue generated from sales over time
                    </div>
                  </div>

                </div>

                <div
                  style={{
                    width: "100%",
                    height: "320px",
                    paddingTop: "15px",
                  }}
                >

                  {loading ? (

                    <div style={emptyStateStyle}>
                      Loading chart...
                    </div>

                  ) : revenueTrendData.length === 0 ? (

                    <div style={emptyStateStyle}>
                      No sales data available.
                    </div>

                  ) : (

                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >

                      <LineChart
                        data={revenueTrendData}
                        margin={{
                          top: 10,
                          right: 20,
                          left: 10,
                          bottom: 10,
                        }}
                      >

                        <CartesianGrid
                          strokeDasharray="3 3"
                        />

                        <XAxis
                          dataKey="date"
                        />

                        <YAxis />

                        <Tooltip
                          formatter={(value) =>
                            formatCurrency(value)
                          }
                        />

                        <Legend />

                        <Line
                          type="monotone"
                          dataKey="revenue"
                          name="Revenue"
                          stroke="#2563eb"
                          strokeWidth={3}
                          dot={{
                            r: 4,
                          }}
                          activeDot={{
                            r: 6,
                          }}
                        />

                      </LineChart>

                    </ResponsiveContainer>

                  )}

                </div>

              </div>

              {/* INVENTORY STATUS */}

              <div className="data-card">

                <div className="data-card-header">

                  <div>
                    <strong>
                      Inventory Status
                    </strong>

                    <div
                      style={{
                        fontSize: "12px",
                        color: "#9ca3af",
                        marginTop: "4px",
                      }}
                    >
                      Low stock vs healthy stock
                    </div>
                  </div>

                </div>

                <div
                  style={{
                    width: "100%",
                    height: "320px",
                  }}
                >

                  {loading ? (

                    <div style={emptyStateStyle}>
                      Loading chart...
                    </div>

                  ) : products.length === 0 ? (

                    <div style={emptyStateStyle}>
                      No inventory data available.
                    </div>

                  ) : (

                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >

                      <PieChart>

                        <Pie
                          data={stockChartData}
                          dataKey="value"
                          nameKey="name"
                          cx="50%"
                          cy="50%"
                          outerRadius={105}
                          innerRadius={55}
                          paddingAngle={4}
                          label
                        >

                          <Cell fill="#f59e0b" />
                          <Cell fill="#22c55e" />

                        </Pie>

                        <Tooltip />

                        <Legend />

                      </PieChart>

                    </ResponsiveContainer>

                  )}

                </div>

              </div>

            </div>

            {/* ==================================================
                LOW STOCK TABLE
            ================================================== */}

            <div className="data-card report-table-card">

              <div className="data-card-header">

                <strong>
                  Low Stock Products
                </strong>

                <span>
                  {lowStockProducts.length} items
                </span>

              </div>

              {lowStockProducts.length === 0 ? (

                <div style={emptyStateStyle}>
                  No low-stock products.
                </div>

              ) : (

                <div className="table-scroll">

                  <table className="management-table">

                    <thead>
                      <tr>
                        <th>Product ID</th>
                        <th>Product</th>
                        <th>Category</th>
                        <th>Price</th>
                        <th>Stock</th>
                      </tr>
                    </thead>

                    <tbody>

                      {lowStockProducts.map(
                        (product) => (

                          <tr
                            key={product.product_id}
                          >

                            <td>
                              <strong className="blue-id">
                                {product.product_id}
                              </strong>
                            </td>

                            <td>
                              {product.name}
                            </td>

                            <td>
                              {product.category}
                            </td>

                            <td>
                              {formatCurrency(
                                product.price
                              )}
                            </td>

                            <td>

                              {product.quantity === 0 ? (

                                <span className="status-danger">
                                  Out of Stock
                                </span>

                              ) : (

                                <span className="status-warning">
                                  {product.quantity} left
                                </span>

                              )}

                            </td>

                          </tr>

                        )
                      )}

                    </tbody>

                  </table>

                </div>

              )}

            </div>

          </section>

        )}

      </main>

      {/* ========================================================
          PRODUCT FORM MODAL
      ======================================================== */}

      {showProductForm && (

        <div className="modal-overlay">

          <div className="modal">

            <div className="modal-header">

              <div>

                <h2>
                  {editingProduct
                    ? "Edit Product"
                    : "Add Product"}
                </h2>

                <p>
                  {editingProduct
                    ? "Update product information"
                    : "Add a new product to inventory"}
                </p>

              </div>

              <button
                onClick={closeProductForm}
                className="modal-close"
              >
                ×
              </button>

            </div>

            <form
              onSubmit={handleProductSubmit}
              className="modal-form"
            >

              {!editingProduct && (

                <div className="form-group">

                  <label>Product ID</label>

                  <input
                    name="product_id"
                    value={productForm.product_id}
                    onChange={handleProductInput}
                    placeholder="Example: P021"
                  />

                </div>

              )}

              <div className="form-group">

                <label>Product Name</label>

                <input
                  name="name"
                  value={productForm.name}
                  onChange={handleProductInput}
                  placeholder="Example: Wireless Keyboard"
                />

              </div>

              <div className="form-group">

                <label>Category</label>

                <input
                  name="category"
                  value={productForm.category}
                  onChange={handleProductInput}
                  placeholder="Example: Electronics"
                />

              </div>

              <div className="form-two-columns">

                <div className="form-group">

                  <label>Price</label>

                  <input
                    name="price"
                    type="number"
                    min="0"
                    step="0.01"
                    value={productForm.price}
                    onChange={handleProductInput}
                    placeholder="0.00"
                  />

                </div>

                <div className="form-group">

                  <label>Quantity</label>

                  <input
                    name="quantity"
                    type="number"
                    min="0"
                    step="1"
                    value={productForm.quantity}
                    onChange={handleProductInput}
                    placeholder="0"
                  />

                </div>

              </div>

              {productError && (
                <div style={modalErrorStyle}>
                  {productError}
                </div>
              )}

              {productMessage && (
                <div style={modalSuccessStyle}>
                  {productMessage}
                </div>
              )}

              <div className="modal-actions">

                <button
                  type="button"
                  onClick={closeProductForm}
                  className="cancel-button"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="primary-button"
                >
                  {editingProduct
                    ? "Update Product"
                    : "Add Product"}
                </button>

              </div>

            </form>

          </div>

        </div>

      )}

      {/* ========================================================
          CUSTOMER FORM MODAL
      ======================================================== */}

      {showCustomerForm && (

        <div className="modal-overlay">

          <div className="modal">

            <div className="modal-header">

              <div>

                <h2>
                  {editingCustomer
                    ? "Edit Customer"
                    : "Add Customer"}
                </h2>

                <p>
                  {editingCustomer
                    ? "Update customer information"
                    : "Add a new customer"}
                </p>

              </div>

              <button
                onClick={closeCustomerForm}
                className="modal-close"
              >
                ×
              </button>

            </div>

            <form
              onSubmit={handleCustomerSubmit}
              className="modal-form"
            >

              {!editingCustomer && (

                <div className="form-group">

                  <label>Customer ID</label>

                  <input
                    name="customer_id"
                    value={customerForm.customer_id}
                    onChange={handleCustomerInput}
                    placeholder="Example: C016"
                  />

                </div>

              )}

              <div className="form-group">

                <label>Customer Name</label>

                <input
                  name="name"
                  value={customerForm.name}
                  onChange={handleCustomerInput}
                  placeholder="Example: Rahul Sharma"
                />

              </div>

              <div className="form-group">

                <label>Phone Number</label>

                <input
                  name="phone"
                  type="tel"
                  maxLength="10"
                  value={customerForm.phone}
                  onChange={handleCustomerInput}
                  placeholder="Example: 9876543225"
                />

              </div>

              {customerError && (
                <div style={modalErrorStyle}>
                  {customerError}
                </div>
              )}

              {customerMessage && (
                <div style={modalSuccessStyle}>
                  {customerMessage}
                </div>
              )}

              <div className="modal-actions">

                <button
                  type="button"
                  onClick={closeCustomerForm}
                  className="cancel-button"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="customer-primary-button"
                >
                  {editingCustomer
                    ? "Update Customer"
                    : "Add Customer"}
                </button>

              </div>

            </form>

          </div>

        </div>

      )}

      {/* ========================================================
          SALES FORM MODAL
      ======================================================== */}

      {showSaleForm && (

        <div className="modal-overlay">

          <div className="modal">

            <div className="modal-header">

              <div>

                <h2>Create Sale</h2>

                <p>
                  Record a new sales transaction
                </p>

              </div>

              <button
                onClick={closeSaleForm}
                className="modal-close"
              >
                ×
              </button>

            </div>

            <form
              onSubmit={handleSaleSubmit}
              className="modal-form"
            >

              <div className="form-group">

                <label>Customer</label>

                <select
                  name="customer_id"
                  value={saleForm.customer_id}
                  onChange={handleSaleInput}
                >

                  <option value="">
                    Select customer
                  </option>

                  {customers.map((customer) => (

                    <option
                      key={customer.customer_id}
                      value={customer.customer_id}
                    >
                      {customer.customer_id} -{" "}
                      {customer.name}
                    </option>

                  ))}

                </select>

              </div>

              <div className="form-group">

                <label>Product</label>

                <select
                  name="product_id"
                  value={saleForm.product_id}
                  onChange={handleSaleInput}
                >

                  <option value="">
                    Select product
                  </option>

                  {products.map((product) => (

                    <option
                      key={product.product_id}
                      value={product.product_id}
                      disabled={product.quantity === 0}
                    >
                      {product.product_id} -{" "}
                      {product.name}{" "}
                      ({product.quantity} in stock)
                    </option>

                  ))}

                </select>

              </div>

              {selectedSaleProduct && (

                <div className="sale-product-info">

                  <div>
                    <span>Price</span>

                    <strong>
                      {formatCurrency(
                        selectedSaleProduct.price
                      )}
                    </strong>
                  </div>

                  <div>
                    <span>Available Stock</span>

                    <strong>
                      {selectedSaleProduct.quantity}
                    </strong>
                  </div>

                </div>

              )}

              <div className="form-group">

                <label>Quantity</label>

                <input
                  name="quantity"
                  type="number"
                  min="1"
                  step="1"
                  value={saleForm.quantity}
                  onChange={handleSaleInput}
                  placeholder="Enter quantity"
                />

              </div>

              <div className="sale-total-box">

                <span>Estimated Total</span>

                <strong>
                  {formatCurrency(
                    saleEstimatedTotal
                  )}
                </strong>

              </div>

              {saleError && (
                <div style={modalErrorStyle}>
                  {saleError}
                </div>
              )}

              {saleMessage && (
                <div style={modalSuccessStyle}>
                  {saleMessage}
                </div>
              )}

              <div className="modal-actions">

                <button
                  type="button"
                  onClick={closeSaleForm}
                  className="cancel-button"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="sale-primary-button"
                >
                  Record Sale
                </button>

              </div>

            </form>

          </div>

        </div>

      )}

    </div>
  );
}

// ============================================================
// INLINE STYLES
// ============================================================

const errorBoxStyle = {
  background: "#fef2f2",
  color: "#dc2626",
  padding: "12px 16px",
  borderRadius: "8px",
  marginBottom: "20px",
  border: "1px solid #fecaca",
  fontSize: "13px",
};

const successBoxStyle = {
  background: "#f0fdf4",
  color: "#15803d",
  border: "1px solid #bbf7d0",
  padding: "11px 15px",
  borderRadius: "8px",
  marginBottom: "15px",
  fontSize: "13px",
};

const modalErrorStyle = {
  background: "#fef2f2",
  color: "#dc2626",
  border: "1px solid #fecaca",
  padding: "9px 12px",
  borderRadius: "6px",
  marginBottom: "15px",
  fontSize: "12px",
};

const modalSuccessStyle = {
  background: "#f0fdf4",
  color: "#15803d",
  border: "1px solid #bbf7d0",
  padding: "9px 12px",
  borderRadius: "6px",
  marginBottom: "15px",
  fontSize: "12px",
};

const emptyStateStyle = {
  padding: "50px",
  textAlign: "center",
  color: "#9ca3af",
  fontSize: "13px",
};

export default App;