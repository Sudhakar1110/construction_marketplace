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

// ==================== PAGE INITIALIZATION ====================

$(document).ready(function() {
    // Initialize cart badge
    construction_marketplace.cart.initBadge();

    // Initialize search
    construction_marketplace.search.init();

    // Handle remove from cart buttons (delegated)
    $(document).on('click', '.remove-cart-btn', function() {
        var materialId = $(this).data('material');
        var priceId = $(this).data('price');
        var row = $(this).closest('tr');
        construction_marketplace.cart.removeFromCart(materialId, priceId, function() {
            row.fadeOut(300, function() { $(this).remove(); });
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
