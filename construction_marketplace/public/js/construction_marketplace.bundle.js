// Copyright (c) 2024, Sudhakar and contributors
// For license information, please see license.txt

// Construction Marketplace JS Bundle
// Complete Website Functionality

frappe.provide("construction_marketplace");
frappe.provide("construction_marketplace.utils");

// ==================== UTILITY FUNCTIONS ====================

construction_marketplace.utils = {
    formatCurrency: function(amount) {
        if (amount === null || amount === undefined) return '0';
        return Number(amount).toLocaleString('en-IN', {
            maximumFractionDigits: 2,
            minimumFractionDigits: 0
        });
    },

    showToast: function(message, type) {
        type = type || 'info';
        var container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        var toast = document.createElement('div');
        toast.className = 'toast-custom ' + type;
        var icons = { success: 'fa-check-circle', error: 'fa-exclamation-circle', info: 'fa-info-circle' };
        toast.innerHTML = '<i class="fas ' + (icons[type] || icons.info) + ' me-2"></i> ' + message;
        container.appendChild(toast);
        setTimeout(function() { toast.style.opacity = '0'; toast.style.transform = 'translateX(100px)'; toast.style.transition = 'all 0.3s ease'; setTimeout(function() { toast.remove(); }, 300); }, 4000);
    },

    getUrlParam: function(name) {
        var url = new URLSearchParams(window.location.search);
        return url.get(name) || '';
    }
};

// ==================== CART FUNCTIONALITY ====================

construction_marketplace.cart = {
    addToCart: function(materialId, priceId, quantity, callback) {
        frappe.call({
            method: "construction_marketplace.api.add_to_cart",
            args: {
                material_id: materialId,
                price_id: priceId,
                quantity: quantity || 1
            },
            callback: function(r) {
                if (r.message && r.message.success) {
                    construction_marketplace.utils.showToast(r.message.message || 'Added to cart!', 'success');
                    construction_marketplace.cart.updateBadge(r.message.item_count);
                    if (callback) callback(r.message);
                }
            },
            error: function() {
                construction_marketplace.utils.showToast('Please login to add items to cart', 'error');
            }
        });
    },

    removeFromCart: function(materialId, priceId, callback) {
        frappe.call({
            method: "construction_marketplace.api.remove_from_cart",
            args: { material_id: materialId, price_id: priceId },
            callback: function(r) {
                if (r.message && r.message.success) {
                    construction_marketplace.utils.showToast('Item removed from cart', 'info');
                    construction_marketplace.cart.updateBadge(r.message.item_count);
                    if (callback) callback(r.message);
                }
            }
        });
    },

    getCart: function(callback) {
        frappe.call({
            method: "construction_marketplace.api.get_cart",
            callback: function(r) {
                if (r.message && callback) callback(r.message);
            }
        });
    },

    updateBadge: function(count) {
        $('.cart-badge').remove();
        if (count > 0) {
            $('.cart-link').append('<span class="badge bg-danger rounded-pill cart-badge ms-1" style="font-size:0.7rem;">' + count + '</span>');
        }
    },

    initBadge: function() {
        frappe.call({
            method: "construction_marketplace.api.get_cart",
            callback: function(r) {
                if (r.message && r.message.items) {
                    construction_marketplace.cart.updateBadge(r.message.items.length);
                }
            }
        });
    }
};

// ==================== SEARCH FUNCTIONALITY ====================

construction_marketplace.search = {
    init: function() {
        var searchInput = document.getElementById('navbar-search');
        if (searchInput) {
            searchInput.addEventListener('keyup', function(e) {
                if (e.keyCode === 13) {
                    var query = this.value.trim();
                    if (query) {
                        window.location.href = '/materials?query=' + encodeURIComponent(query);
                    }
                }
            });
        }
    }
};

// ==================== FLOATING CART WIDGET ====================

construction_marketplace.floatingCart = {
    isOpen: false,

    createWidget: function() {
        // Don't create if already exists
        if ($('#floating-cart-widget').length) return;

        var html = '';
        html += '<div id="floating-cart-widget">';
        html += '<div class="mini-cart-overlay" id="mini-cart-overlay"></div>';
        html += '<button class="floating-cart-btn" id="floating-cart-btn" title="View Cart">';
        html += '<i class="fas fa-shopping-cart"></i>';
        html += '<span class="cart-count d-none" id="cart-count-badge">0</span>';
        html += '</button>';
        html += '<div class="mini-cart-panel" id="mini-cart-panel">';
        html += '<div class="mini-cart-header">';
        html += '<h6><i class="fas fa-shopping-cart me-2"></i>Shopping Cart</h6>';
        html += '<button class="close-btn" id="mini-cart-close"><i class="fas fa-times"></i></button>';
        html += '</div>';
        html += '<div class="mini-cart-body" id="mini-cart-body">';
        html += '<div class="mini-cart-empty">';
        html += '<i class="fas fa-shopping-cart"></i>';
        html += '<p>Your cart is empty</p>';
        html += '</div>';
        html += '</div>';
        html += '<div class="mini-cart-footer d-none" id="mini-cart-footer">';
        html += '<div class="mini-cart-total">';
        html += '<span>Total</span>';
        html += '<span class="total-value" id="mini-cart-total">₹ 0</span>';
        html += '</div>';
        html += '<a href="/checkout" class="mini-cart-checkout-btn">';
        html += '<i class="fas fa-credit-card me-2"></i>Proceed to Checkout</a>';
        html += '</div>';
        html += '</div></div>';

        $('body').append(html);

        // Bind events
        this.bindEvents();
    },

    bindEvents: function() {
        var self = this;

        $('#floating-cart-btn').on('click', function(e) {
            e.stopPropagation();
            self.togglePanel();
        });

        $('#mini-cart-close, #mini-cart-overlay').on('click', function() {
            self.hidePanel();
        });

        // Refresh cart icon badge on page visibility change
        $(document).on('cart-updated', function() {
            self.refreshBadge();
        });
    },

    refreshBadge: function() {
        var self = this;
        frappe.call({
            method: "construction_marketplace.api.get_cart",
            callback: function(r) {
                if (r.message && r.message.items && r.message.items.length > 0) {
                    var count = r.message.items.length;
                    $('#cart-count-badge').text(count).removeClass('d-none');
                    $('#floating-cart-btn').addClass('has-items').css('display', 'flex');
                } else {
                    $('#cart-count-badge').addClass('d-none');
                    $('#floating-cart-btn').removeClass('has-items');
                    // Still show if user is logged in but cart empty
                    if (r.message && r.message.items) {
                        $('#floating-cart-btn').css('display', 'flex');
                    }
                }
            }
        });
    },

    loadCartItems: function() {
        var self = this;
        $('#mini-cart-body').html('<div class="text-center py-4"><div class="spinner-border spinner-border-sm text-primary" role="status"></div><p class="mt-2 small text-muted">Loading...</p></div>');

        frappe.call({
            method: "construction_marketplace.api.get_cart",
            callback: function(r) {
                if (r.message && r.message.items && r.message.items.length > 0) {
                    var items = r.message.items;
                    var bodyHtml = '';
                    items.forEach(function(item) {
                        bodyHtml += '<div class="mini-cart-item">';
                        bodyHtml += '<div class="item-icon"><i class="fas fa-cube"></i></div>';
                        bodyHtml += '<div class="item-info">';
                        bodyHtml += '<div class="item-name">' + (item.material_name || 'Item') + '</div>';
                        bodyHtml += '<div class="item-meta">Qty: ' + item.quantity + ' × ₹ ' + construction_marketplace.utils.formatCurrency(item.rate || 0) + '</div>';
                        bodyHtml += '</div>';
                        bodyHtml += '<div class="item-amount">₹ ' + construction_marketplace.utils.formatCurrency(item.amount || 0) + '</div>';
                        bodyHtml += '</div>';
                    });
                    $('#mini-cart-body').html(bodyHtml);
                    $('#mini-cart-total').text('₹ ' + construction_marketplace.utils.formatCurrency(r.message.total || 0));
                    $('#mini-cart-footer').removeClass('d-none');
                } else if (r.message && r.message.items && r.message.items.length === 0) {
                    $('#mini-cart-body').html('<div class="mini-cart-empty"><i class="fas fa-shopping-cart"></i><p>Your cart is empty</p></div>');
                    $('#mini-cart-footer').addClass('d-none');
                } else {
                    // Not logged in
                    $('#mini-cart-body').html('<div class="mini-cart-empty"><i class="fas fa-user-lock"></i><p>Please login to view cart</p><a href="/login" class="btn btn-primary btn-sm rounded-pill mt-2 px-4">Login</a></div>');
                    $('#mini-cart-footer').addClass('d-none');
                }
            },
            error: function() {
                $('#mini-cart-body').html('<div class="mini-cart-empty"><i class="fas fa-exclamation-circle"></i><p>Could not load cart</p></div>');
                $('#mini-cart-footer').addClass('d-none');
            }
        });
    },

    togglePanel: function() {
        if (this.isOpen) {
            this.hidePanel();
        } else {
            this.showPanel();
        }
    },

    showPanel: function() {
        this.isOpen = true;
        $('#mini-cart-overlay').addClass('active');
        $('#mini-cart-panel').addClass('active');
        this.loadCartItems();
    },

    hidePanel: function() {
        this.isOpen = false;
        $('#mini-cart-overlay').removeClass('active');
        $('#mini-cart-panel').removeClass('active');
    }
};

// ==================== PAGE INITIALIZATION ====================

$(document).ready(function() {
    // Initialize floating cart widget
    construction_marketplace.floatingCart.createWidget();

    // Initialize cart badge
    construction_marketplace.cart.initBadge();

    // Initialize floating cart badge
    setTimeout(function() {
        construction_marketplace.floatingCart.refreshBadge();
    }, 500);

    // Initialize search
    construction_marketplace.search.init();

    // Handle remove from cart buttons (delegated)
    $(document).on('click', '.remove-cart-btn', function() {
        var materialId = $(this).data('material');
        var priceId = $(this).data('price');
        var row = $(this).closest('tr');
        construction_marketplace.cart.removeFromCart(materialId, priceId, function() {
            row.fadeOut(300, function() { $(this).remove(); });
            $(document).trigger('cart-updated');
        });
    });

    // Handle add to cart buttons (delegated)
    $(document).on('click', '.add-to-cart-btn', function() {
        var btn = $(this);
        var materialId = btn.data('material');
        var priceId = btn.data('price');
        var qty = btn.data('qty') || 1;

        btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-1"></i>');
        construction_marketplace.cart.addToCart(materialId, priceId, qty, function() {
            btn.html('<i class="fas fa-check me-1"></i> Added').removeClass('btn-primary').addClass('btn-success');
            setTimeout(function() {
                btn.html('<i class="fas fa-shopping-cart me-1"></i> Add').prop('disabled', false).removeClass('btn-success').addClass('btn-primary');
            }, 2000);
            $(document).trigger('cart-updated');
        });
    });

    // Apply smooth scroll to all internal links
    $(document).on('click', 'a[href^="#"]', function(e) {
        var target = $($(this).attr('href'));
        if (target.length) {
            e.preventDefault();
            $('html, body').animate({ scrollTop: target.offset().top - 80 }, 500);
        }
    });

    // Add fade-in-up animation to cards
    $('.product-card, .category-card, .supplier-card, .testimonial-card, .contractor-card, .architect-card, .designer-card, .project-card, .price-card').each(function(i) {
        $(this).addClass('fade-in-up');
    });
});

// ==================== FRAPPE DESKTOP DASHBOARD ====================

frappe.pages["construction-marketplace-dashboard"].onload = function(wrapper) {
    frappe.call({
        method: "construction_marketplace.construction_marketplace.utils.get_dashboard_data",
        callback: function(r) {
            if (r.message) {
                // Render dashboard with data
            }
        }
    });
};

frappe.form.formatters["Material Category"] = function(value, doc, fieldname) {
    if (value) {
        return '<span class="cm-category-badge">' + value + '</span>';
    }
    return value;
};

$(document).on("form-render", function(e, wrapper) {
    if (wrapper.data && wrapper.data.doctype === "Marketplace Order") {
        var status = wrapper.data.status;
        if (status) {
            wrapper.$wrapper.find(".page-title")
                .addClass("order-status-" + status.toLowerCase());
        }
    }
});
