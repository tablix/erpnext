// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// shopping cart
<<<<<<< HEAD
frappe.provide("erpnext.shopping_cart");
var shopping_cart = erpnext.shopping_cart;

frappe.ready(function() {
	var full_name = frappe.session && frappe.session.user_fullname;
	// update user
	if(full_name) {
		$('.navbar li[data-label="User"] a')
			.html('<i class="fa fa-fixed-width fa fa-user"></i> ' + full_name);
	}

=======
frappe.provide("shopping_cart");

frappe.ready(function() {
	// update user
	if(full_name) {
		$('.navbar li[data-label="User"] a')
			.html('<i class="icon-fixed-width icon-user"></i> ' + full_name);
	}
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	// update login
	shopping_cart.show_shoppingcart_dropdown();
	shopping_cart.set_cart_count();
	shopping_cart.bind_dropdown_cart_buttons();
});

$.extend(shopping_cart, {
	show_shoppingcart_dropdown: function() {
		$(".shopping-cart").on('shown.bs.dropdown', function() {
			if (!$('.shopping-cart-menu .cart-container').length) {
				return frappe.call({
					method: 'erpnext.shopping_cart.cart.get_shopping_cart_menu',
					callback: function(r) {
						if (r.message) {
							$('.shopping-cart-menu').html(r.message);
						}
					}
				});
			}
		});
	},
<<<<<<< HEAD

	update_cart: function(opts) {
		if(frappe.session.user==="Guest") {
=======
	
	update_cart: function(opts) {
		if(!full_name || full_name==="Guest") {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
			if(localStorage) {
				localStorage.setItem("last_visited", window.location.pathname);
			}
			window.location.href = "/login";
		} else {
			return frappe.call({
				type: "POST",
				method: "erpnext.shopping_cart.cart.update_cart",
				args: {
					item_code: opts.item_code,
					qty: opts.qty,
					with_items: opts.with_items || 0
				},
				btn: opts.btn,
				callback: function(r) {
<<<<<<< HEAD
					shopping_cart.set_cart_count();
					if (r.message.shopping_cart_menu) {
						$('.shopping-cart-menu').html(r.message.shopping_cart_menu);
					}
=======
					shopping_cart.set_cart_count();	
					if (r.message.shopping_cart_menu) {
						$('.shopping-cart-menu').html(r.message.shopping_cart_menu);
					}					
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
					if(opts.callback)
						opts.callback(r);
				}
			});
		}
	},

	set_cart_count: function() {
		var cart_count = getCookie("cart_count");
<<<<<<< HEAD

		if(cart_count) {
			$(".shopping-cart").toggleClass('hidden', false);
		}

=======
		
		if(cart_count) {
			$(".shopping-cart").toggle(true);	
		}		
		
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		var $cart = $('.cart-icon');
		var $badge = $cart.find("#cart-count");

		if(parseInt(cart_count) === 0 || cart_count === undefined) {
			$cart.css("display", "none");
			$(".cart-items").html('Cart is Empty');
			$(".cart-tax-items").hide();
			$(".btn-place-order").hide();
			$(".cart-addresses").hide();
		}
		else {
			$cart.css("display", "inline");
		}

		if(cart_count) {
			$badge.html(cart_count);
		} else {
			$badge.remove();
		}
	},
<<<<<<< HEAD

=======
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
	shopping_cart_update: function(item_code, newVal, cart_dropdown) {
		frappe.freeze();
		shopping_cart.update_cart({
			item_code: item_code,
			qty: newVal,
			with_items: 1,
			btn: this,
			callback: function(r) {
				frappe.unfreeze();
				if(!r.exc) {
					$(".cart-items").html(r.message.items);
					$(".cart-tax-items").html(r.message.taxes);
					if (cart_dropdown != true) {
						$(".cart-icon").hide();
<<<<<<< HEAD
					}
=======
					}					
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
				}
			},
		});
	},
<<<<<<< HEAD


	bind_dropdown_cart_buttons: function () {
=======
	
	
	bind_dropdown_cart_buttons: function() {
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
		$(".cart-icon").on('click', '.number-spinner button', function () {
			var btn = $(this),
				input = btn.closest('.number-spinner').find('input'),
				oldValue = input.val().trim(),
				newVal = 0;
<<<<<<< HEAD

			if (btn.attr('data-dir') == 'up') {
				newVal = parseInt(oldValue) + 1;
			} else {
				if (oldValue > 1) {
					newVal = parseInt(oldValue) - 1;
				}
			}
			input.val(newVal);
			var item_code = input.attr("data-item-code");
			shopping_cart.shopping_cart_update(item_code, newVal, true);
			return false;
		});

	},

=======
			
				if (btn.attr('data-dir') == 'up') {
					newVal = parseInt(oldValue) + 1;
				} else {
					if (oldValue > 1) {
						newVal = parseInt(oldValue) - 1;
					}
			}
			input.val(newVal);
			var item_code = input.attr("data-item-code"); 
			shopping_cart.shopping_cart_update(item_code, newVal, true);
			return false;
		});
		
	},
	
>>>>>>> ccaba6a395ce8e0526cc059982c83eddcdec9347
});
