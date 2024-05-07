$(document).ready(function(){
// smooth scroll
$('a').smoothScroll({
	speed: 900
});

//set slider
//*************************************
	var slider = $(".slider"),
		pointerPrev = $(".pointer_prev"),
		pointerNext = $(".pointer_next");
		
	
  	slider.slick({
		arrows: true,
		fade: true,
		prevArrow: $(".pointer_prev"),
		nextArrow: $(".pointer_next")
	});

  	// animate text inside slide
  	// initialize text to animate
  	$('.item__text').textillate({
  			in: {
  				effect: 'rollIn',
  				delay: 5
  				},
  			loop: false
  		});
  	// set callbacks on swipe slider
	slider.on('init', function(event, slick, currentSlide){
  		$('.item__text').textillate('start');
	});

	slider.on('beforeChange', function(event, slick, currentSlide, nextSlide){
		var sliderItems = $(this).find('.slider__item');
		$(sliderItems[nextSlide]).find('.item__text').css({opacity: 0});
	});

	slider.on('afterChange', function(event, slick, currentSlide){
		var sliderItems = $(this).find('.slider__item');
		$(sliderItems[currentSlide]).find('.item__text').css({opacity: 1});
		
  		$('.item__text').textillate('start');
	});
	
//slider arrows appear
//*************************************
	slider.on('mouseover', function(){
		pointerPrev.addClass("pointer_prev_show");
		pointerNext.addClass("pointer_next_show");
	});
	$(".pointer").on('mouseover', function(){
		pointerPrev.addClass("pointer_prev_show");
		pointerNext.addClass("pointer_next_show");
	});
	$(".pointer-container").on('mouseover', function(){
		pointerPrev.addClass("pointer_prev_show");
		pointerNext.addClass("pointer_next_show");
	});
	
//slider arrows hide
//*************************************
	slider.on('mouseleave', function(){
		pointerPrev.removeClass("pointer_prev_show");
		pointerNext.removeClass("pointer_next_show");
	});
	
//	start plaing video
//	***********************************
	$(".poster__play-button").on('click', function(){
		$(".video__item_poster").addClass("poster_hide");
		$("iframe.video__item").attr("src", "https://player.vimeo.com/video/212731897?	color=ffffff&title=0&byline=0&autoplay=1");
	});
	
//	services owl-carousel
//	***********************************
		var owl = $("#services .owl-carousel"),
		next = $(".arrow_front"),
		prev = $(".arrow_back");

		owl.owlCarousel({
			loop: true,
			margin: 10,
			responsiveClass: true,
			rewind: false,
			dots: false,
			responsive: {
				0: {
					items:1
				},
				480: {
					items:2
				},
				1024: {
					items:3
				}
			}
		});

		// Go to the next item
		$('.arrow_front').click(function(event) {
		    owl.trigger('next.owl.carousel');
		});

		// Go to the previous item
		$('.arrow_back').click(function(event) {
		    // With optional speed parameter
		    // Parameters has to be in square bracket '[]'
		    owl.trigger('prev.owl.carousel', [300]);
		});
	
//	clients owl-carousel setup
//	***********************************
		var owl2 = $("#clients .owl-carousel"),
			clientsItems = $("#clients .item").length,
			clientsCurrentItem = 1;

		// get counter items
		var current = $('.clients__counter__item1'),
			allCount = $('.clients__counter__item2');

			allCount.text(clientsItems);
			current.text(clientsCurrentItem);

		owl2.owlCarousel({
			loop: true,
			margin: 10,
			responsiveClass: true,
			rewind: false,
			dots: false,
			items: 1
		});

		// Go to the next item
		$('.clients__arrow_next').click(function(event) {
			if(clientsCurrentItem == clientsItems) {
				clientsCurrentItem = 1;
				current.text(clientsCurrentItem);
				owl2.trigger('next.owl.carousel');
			} else {
				clientsCurrentItem++;
				current.text(clientsCurrentItem);
				owl2.trigger('next.owl.carousel');
			}
		});

		// Go to the previous item
		$('.clients__arrow_back').click(function(event) {
			if(clientsCurrentItem == 1) {
				clientsCurrentItem = clientsItems;
				current.text(clientsCurrentItem);
				owl2.trigger('prev.owl.carousel', [300]);
			} else {
				clientsCurrentItem--;
				current.text(clientsCurrentItem);
				// With optional speed parameter
		    	// Parameters has to be in square bracket '[]'
		    	owl2.trigger('prev.owl.carousel', [300]);
			}
		});
	
//	gallery isotope filtering
//	************************************
		var galleryContainer = $(".gallery__items"),
			isotopFilterButtons = $(".works__nav__item");
	
		isotopFilterButtons.on('click', function(){
			var filterValue = $(this).attr('data-filter');
			
			galleryContainer.isotope({
				filter: filterValue
			});
			
			for(var i = 0; i < isotopFilterButtons.length; i++){
				$(isotopFilterButtons[i]).removeClass('works__nav__item_active');
			}
			
			$(this).addClass('works__nav__item_active');
		});
	
//	gallery magnific popup
//	************************************
		var magnificPopup = $.magnificPopup.instance;

		$('.gallery__items').magnificPopup({
			delegate: '.item__hover__zoom',
			type: 'image',
			gallery: {
				enabled: true,
				navigateByImgClick: false,  // for correct counter working
				preload: [0, 2],
				tCounter: '<span class="popup-counter">%curr% / %total%</span>',
				arrowMarkup: ''
			},
			zoom: {
				enabled: true,
				duration: 300, // don't foget to change the duration also in CSS
				opener: function(element) {
					return element.find('img');
				}
			},
			image: {
				verticalFit: true,
				titleSrc: function(item) {
					return item.el.attr('title');
				}
			},
			callbacks: {
				open: function(){
					movePopup();
				},
				change: function(){
					// append popup's controls
    				$(this.content).find('.mfp-counter').append('<div class="popup__arrow popup__arrow_next"><div class="popup__arrow__line-short popup__arrow__line-up"></div><div class="popup__arrow__line"></div><div class="popup__arrow__line-short popup__arrow__line-down"></div></div>');
    				$(this.content).find('.mfp-counter').prepend('<div class="popup__arrow popup__arrow_back"><div class="popup__arrow__line-short popup__arrow__line-up"></div><div class="popup__arrow__line"></div><div class="popup__arrow__line-short popup__arrow__line-down"></div></div>');
				}
			}
		});

		// change image by click on arrow
		function movePopup() {
			if(magnificPopup.index + 1 == magnificPopup.items.length)
    			$('.popup__arrow_next').addClass('popup__arrow_gray');
    		else if(magnificPopup.index == 0)
    			$('.popup__arrow_back').addClass('popup__arrow_gray');

    		$('.popup__arrow_next').click(function(){
    			if(magnificPopup.index + 1 == magnificPopup.items.length)
    				return;
    			else {
    				magnificPopup.next();
    				movePopup();
    			}
    		});

    		$('.popup__arrow_back').click(function(){
    			if(magnificPopup.index == 0)
    				return;
    			else {
    				magnificPopup.prev();
    				movePopup();
    			}
    		});
    	}
});