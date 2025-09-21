// Main JavaScript for E-commerce Store

// Global variables
let currentUser = null;
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let currentPage = 1;
let isLoading = false;
let hasMoreProducts = true;

// API Configuration
const API_BASE_URL = '/api';
const API_ENDPOINTS = {
    auth: {
        login: `${API_BASE_URL}/auth/login/`,
        register: `${API_BASE_URL}/auth/register/`,
        profile: `${API_BASE_URL}/auth/profile/`,
        refresh: `${API_BASE_URL}/auth/refresh/`
    },
    products: {
        list: `${API_BASE_URL}/products/`,
        search: `${API_BASE_URL}/products/search/`,
        detail: (id) => `${API_BASE_URL}/products/${id}/`,
        lowStock: `${API_BASE_URL}/products/low_stock/`
    },
    categories: {
        list: `${API_BASE_URL}/categories/`,
        detail: (id) => `${API_BASE_URL}/categories/${id}/`,
        products: (id) => `${API_BASE_URL}/categories/${id}/products/`
    }
};

// Utility Functions
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastBody = document.getElementById('toastBody');
    
    toastBody.textContent = message;
    toast.className = `toast show`;
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

function showLoading() {
    document.getElementById('loadingSpinner').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

function getStockStatus(stock) {
    if (stock === 0) return { text: 'Out of Stock', class: 'bg-danger' };
    if (stock < 10) return { text: `Low Stock (${stock})`, class: 'bg-warning' };
    return { text: `In Stock (${stock})`, class: 'bg-success' };
}

// API Functions
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    // Add authentication token if available
    const token = localStorage.getItem('access_token');
    if (token) {
        defaultOptions.headers['Authorization'] = `Bearer ${token}`;
    }
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, finalOptions);
        
        if (response.status === 401) {
            // Token expired, try to refresh
            await refreshToken();
            // Retry the request with new token
            const newToken = localStorage.getItem('access_token');
            if (newToken) {
                finalOptions.headers['Authorization'] = `Bearer ${newToken}`;
                return await fetch(url, finalOptions);
            }
        }
        
        return response;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

async function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return false;
    
    try {
        const response = await fetch(API_ENDPOINTS.auth.refresh, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return true;
        }
    } catch (error) {
        console.error('Token refresh failed:', error);
    }
    
    // If refresh fails, clear tokens and redirect to login
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    return false;
}

// Authentication Functions
async function login(email, password) {
    try {
        const response = await apiRequest(API_ENDPOINTS.auth.login, {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            currentUser = data.user;
            updateUserInterface();
            showToast('Login successful!', 'success');
            return true;
        } else {
            const error = await response.json();
            showToast(error.non_field_errors?.[0] || 'Login failed', 'error');
            return false;
        }
    } catch (error) {
        showToast('Login failed. Please try again.', 'error');
        return false;
    }
}

async function register(userData) {
    try {
        const response = await apiRequest(API_ENDPOINTS.auth.register, {
            method: 'POST',
            body: JSON.stringify(userData)
        });
        
        if (response.ok) {
            showToast('Registration successful! Please login.', 'success');
            return true;
        } else {
            const error = await response.json();
            const errorMessage = Object.values(error).flat().join(', ');
            showToast(errorMessage, 'error');
            return false;
        }
    } catch (error) {
        showToast('Registration failed. Please try again.', 'error');
        return false;
    }
}

async function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    currentUser = null;
    updateUserInterface();
    showToast('Logged out successfully!', 'success');
}

function updateUserInterface() {
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const profileBtn = document.getElementById('profileBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    
    if (currentUser) {
        loginBtn.style.display = 'none';
        registerBtn.style.display = 'none';
        profileBtn.style.display = 'block';
        logoutBtn.style.display = 'block';
    } else {
        loginBtn.style.display = 'block';
        registerBtn.style.display = 'block';
        profileBtn.style.display = 'none';
        logoutBtn.style.display = 'none';
    }
}

// Product Functions
async function loadProducts(filters = {}) {
    if (isLoading) return;
    
    isLoading = true;
    showLoading();
    
    try {
        const params = new URLSearchParams({
            page: currentPage,
            ...filters
        });
        
        const response = await apiRequest(`${API_ENDPOINTS.products.list}?${params}`);
        
        if (response.ok) {
            const data = await response.json();
            displayProducts(data.results);
            
            hasMoreProducts = data.next !== null;
            updateLoadMoreButton();
        } else {
            showToast('Failed to load products', 'error');
        }
    } catch (error) {
        showToast('Error loading products', 'error');
    } finally {
        isLoading = false;
        hideLoading();
    }
}

async function searchProducts(query, filters = {}) {
    if (isLoading) return;
    
    isLoading = true;
    showLoading();
    
    try {
        const params = new URLSearchParams({
            search: query,
            ...filters
        });
        
        const response = await apiRequest(`${API_ENDPOINTS.products.search}?${params}`);
        
        if (response.ok) {
            const data = await response.json();
            displayProducts(data.results);
            hasMoreProducts = false; // Search results don't have pagination
            updateLoadMoreButton();
        } else {
            showToast('Search failed', 'error');
        }
    } catch (error) {
        showToast('Search error', 'error');
    } finally {
        isLoading = false;
        hideLoading();
    }
}

function displayProducts(products) {
    const productsGrid = document.getElementById('productsGrid');
    
    if (currentPage === 1) {
        productsGrid.innerHTML = '';
    }
    
    products.forEach(product => {
        const productCard = createProductCard(product);
        productsGrid.appendChild(productCard);
    });
}

function createProductCard(product) {
    const col = document.createElement('div');
    col.className = 'col-lg-3 col-md-4 col-sm-6 mb-4';
    
    const stockStatus = getStockStatus(product.stock_quantity);
    
    col.innerHTML = `
        <div class="card product-card h-100" data-product-id="${product.id}">
            <div class="position-relative">
                <img src="${product.image || '/static/images/no-image.png'}" 
                     class="card-img-top product-image" 
                     alt="${product.title}"
                     onerror="this.src='/static/images/no-image.png'">
                <div class="position-absolute top-0 end-0 m-2">
                    <span class="badge ${stockStatus.class} stock-badge">${stockStatus.text}</span>
                </div>
            </div>
            <div class="card-body d-flex flex-column">
                <h5 class="card-title product-title">${product.title}</h5>
                <p class="card-text product-description">${product.description}</p>
                <div class="mt-auto">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <span class="product-price">${formatPrice(product.price)}</span>
                        <small class="text-muted">${product.category.title}</small>
                    </div>
                    <div class="d-grid gap-2">
                        <button class="btn btn-outline-primary btn-sm" onclick="viewProduct(${product.id})">
                            <i class="fas fa-eye me-1"></i>View Details
                        </button>
                        <button class="btn btn-primary btn-sm" onclick="addToCart(${product.id})" 
                                ${product.stock_quantity === 0 ? 'disabled' : ''}>
                            <i class="fas fa-cart-plus me-1"></i>Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    return col;
}

async function viewProduct(productId) {
    try {
        const response = await apiRequest(API_ENDPOINTS.products.detail(productId));
        
        if (response.ok) {
            const product = await response.json();
            showProductModal(product);
        } else {
            showToast('Product not found', 'error');
        }
    } catch (error) {
        showToast('Error loading product', 'error');
    }
}

function showProductModal(product) {
    const modal = new bootstrap.Modal(document.getElementById('productModal'));
    const modalTitle = document.getElementById('productModalTitle');
    const modalBody = document.getElementById('productModalBody');
    
    modalTitle.textContent = product.title;
    
    const stockStatus = getStockStatus(product.stock_quantity);
    
    modalBody.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <img src="${product.image || '/static/images/no-image.png'}" 
                     class="img-fluid rounded" 
                     alt="${product.title}"
                     onerror="this.src='/static/images/no-image.png'">
            </div>
            <div class="col-md-6">
                <h4>${product.title}</h4>
                <p class="text-muted">${product.description}</p>
                <div class="mb-3">
                    <span class="h3 text-success">${formatPrice(product.price)}</span>
                </div>
                <div class="mb-3">
                    <span class="badge ${stockStatus.class}">${stockStatus.text}</span>
                </div>
                <div class="mb-3">
                    <strong>Category:</strong> ${product.category.title}
                </div>
                <div class="mb-3">
                    <strong>SKU:</strong> #${product.id}
                </div>
            </div>
        </div>
    `;
    
    modal.show();
}

// Category Functions
async function loadCategories() {
    try {
        const response = await apiRequest(API_ENDPOINTS.categories.list);
        
        if (response.ok) {
            const data = await response.json();
            displayCategories(data.results);
            populateCategoryFilters(data.results);
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

function displayCategories(categories) {
    const categoriesGrid = document.getElementById('categoriesGrid');
    
    categories.forEach(category => {
        const categoryCard = createCategoryCard(category);
        categoriesGrid.appendChild(categoryCard);
    });
}

function createCategoryCard(category) {
    const col = document.createElement('div');
    col.className = 'col-lg-3 col-md-4 col-sm-6 mb-4';
    
    col.innerHTML = `
        <div class="card category-card h-100" onclick="filterByCategory(${category.id})">
            <img src="${category.image || '/static/images/no-category.png'}" 
                 class="card-img-top category-image" 
                 alt="${category.title}"
                 onerror="this.src='/static/images/no-category.png'">
            <div class="card-body text-center">
                <h5 class="card-title category-title">${category.title}</h5>
                <p class="card-text category-description">${category.description}</p>
            </div>
        </div>
    `;
    
    return col;
}

function populateCategoryFilters(categories) {
    const categorySelects = document.querySelectorAll('#categoryFilter, #productCategoryFilter');
    
    categorySelects.forEach(select => {
        // Clear existing options except the first one
        while (select.children.length > 1) {
            select.removeChild(select.lastChild);
        }
        
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.title;
            select.appendChild(option);
        });
    });
}

// Cart Functions
function addToCart(productId) {
    if (!currentUser) {
        showToast('Please login to add items to cart', 'warning');
        return;
    }
    
    const existingItem = cart.find(item => item.productId === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ productId, quantity: 1 });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    showToast('Item added to cart!', 'success');
}

function updateCartCount() {
    const cartCount = cart.reduce((total, item) => total + item.quantity, 0);
    document.getElementById('cartCount').textContent = cartCount;
}

// Filter Functions
function applyFilters() {
    const filters = {
        ordering: document.getElementById('sortSelect').value,
        category: document.getElementById('productCategoryFilter').value,
        min_price: document.getElementById('minPrice').value,
        max_price: document.getElementById('maxPrice').value
    };
    
    // Remove empty filters
    Object.keys(filters).forEach(key => {
        if (!filters[key]) delete filters[key];
    });
    
    currentPage = 1;
    loadProducts(filters);
}

function clearFilters() {
    document.getElementById('sortSelect').value = '-created_at';
    document.getElementById('productCategoryFilter').value = '';
    document.getElementById('minPrice').value = '';
    document.getElementById('maxPrice').value = '';
    
    currentPage = 1;
    loadProducts();
}

function filterByCategory(categoryId) {
    document.getElementById('productCategoryFilter').value = categoryId;
    applyFilters();
}

// Search Functions
function performSearch() {
    const query = document.getElementById('searchInput').value.trim();
    const categoryId = document.getElementById('categoryFilter').value;
    
    if (query) {
        const filters = {};
        if (categoryId) filters.category = categoryId;
        
        currentPage = 1;
        searchProducts(query, filters);
    } else {
        const filters = {};
        if (categoryId) filters.category = categoryId;
        
        currentPage = 1;
        loadProducts(filters);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize
    updateUserInterface();
    updateCartCount();
    
    // Search form
    document.getElementById('searchForm').addEventListener('submit', function(e) {
        e.preventDefault();
        performSearch();
    });
    
    // Home search form
    const homeSearchForm = document.getElementById('homeSearchForm');
    if (homeSearchForm) {
        homeSearchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = document.getElementById('homeSearchInput').value.trim();
            if (query) {
                window.location.href = `/products/?search=${encodeURIComponent(query)}`;
            }
        });
    }
    
    // Login form
    document.getElementById('loginForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        const success = await login(email, password);
        if (success) {
            bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
            document.getElementById('loginForm').reset();
        }
    });
    
    // Register form
    document.getElementById('registerForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const userData = {
            email: document.getElementById('registerEmail').value,
            username: document.getElementById('registerUsername').value,
            first_name: document.getElementById('registerFirstName').value,
            last_name: document.getElementById('registerLastName').value,
            password: document.getElementById('registerPassword').value,
            password_confirm: document.getElementById('registerPasswordConfirm').value
        };
        
        const success = await register(userData);
        if (success) {
            bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
            document.getElementById('registerForm').reset();
        }
    });
    
    // Modal switches
    document.getElementById('showRegisterModal').addEventListener('click', function(e) {
        e.preventDefault();
        bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
        new bootstrap.Modal(document.getElementById('registerModal')).show();
    });
    
    document.getElementById('showLoginModal').addEventListener('click', function(e) {
        e.preventDefault();
        bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
        new bootstrap.Modal(document.getElementById('loginModal')).show();
    });
    
    // Login/Register buttons
    document.getElementById('loginBtn').addEventListener('click', function(e) {
        e.preventDefault();
        new bootstrap.Modal(document.getElementById('loginModal')).show();
    });
    
    document.getElementById('registerBtn').addEventListener('click', function(e) {
        e.preventDefault();
        new bootstrap.Modal(document.getElementById('registerModal')).show();
    });
    
    // Logout button
    document.getElementById('logoutBtn').addEventListener('click', function(e) {
        e.preventDefault();
        logout();
    });
    
    // Filter buttons
    document.getElementById('applyFilters').addEventListener('click', applyFilters);
    document.getElementById('clearFilters').addEventListener('click', clearFilters);
    
    // Load more button
    document.getElementById('loadMoreBtn').addEventListener('click', function() {
        currentPage++;
        loadProducts();
    });
});

// Initialize functions for specific pages
function initializeHomePage() {
    loadCategories();
    loadProducts();
}

function initializeProductsPage() {
    loadCategories();
    loadProducts();
}

function updateLoadMoreButton() {
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) {
        loadMoreBtn.style.display = hasMoreProducts ? 'block' : 'none';
    }
}
