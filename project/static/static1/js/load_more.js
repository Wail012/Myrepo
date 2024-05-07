;
(function($) {
	jQuery.fn.portfolio_addon = function (addon_options) {
        //Set Variables
        var addon_el = jQuery(this),
            img_count = addon_options.items.length,
            img_per_load = addon_options.load_count,
            $newEls = '',
            alreadyAdded = 0,
            preloader = document.querySelector('.preloader'),
            buttonText = document.querySelector('.button-text');

            // Initialize isotope
            addon_el.isotope();

        $(".gallery__button").on('click', function(){
            // set preloader
            preloader.hidden = false;
            buttonText.hidden = true;
            $(this).addClass("gallery__button_preloading");
        	// set count of loading images
        	img_per_load = addon_options.load_count;
        	// reset last itages set
        	$newEls = '';
        	
        	if(!img_count) {
        		$(this).addClass('gallery__button_disabled');
				$(this).text('No more');

        		return;
        	}

        	if(img_per_load > img_count)
        		img_per_load = img_count;

        	// Already added items
        	alreadyAdded = addon_el.find('.av-added').length;
            // Creating elements
            while(img_per_load) {
            	$newEls += '<div class="av-added gallery__item col-xs-12 col-sm-6 ' + addon_options.items[alreadyAdded].filter + '" style="background-image: url(' + addon_options.items[alreadyAdded].backgroundImage + ')"><div class="gallery__item__hover"><span class="item__hover__line"></span><span class="item__hover__tag">' + addon_options.items[alreadyAdded].tagName + '</span>' + '<h3 class="item__hover__header"><a href="' + addon_options.items[alreadyAdded].headingHref + '">' + addon_options.items[alreadyAdded].heading + '</a></h3><h4 class="item__hover__header-small">' + addon_options.items[alreadyAdded].headingSmall + '</h4><a href="' + addon_options.items[alreadyAdded].img + '" rel="nofollow" class="item__hover__zoom" title="' + addon_options.items[alreadyAdded].title + '"><img src="' + addon_options.items[alreadyAdded].img + '" alt>+&nbsp;Zoom</a></div></div>\n';

            	img_per_load--;
            	alreadyAdded++;
            }

			setTimeout(function(){
                addon_el.isotope('insert', $($newEls));
                preloader.hidden = true;
                buttonText.hidden = false;
                $(this).removeClass("gallery__button_preloading");

                if(alreadyAdded + img_per_load >= img_count) {
                    $(this).addClass('gallery__button_disabled');
                    $(this).text('No more');
                    $(this).off('click');
                }
            }.bind($(this)), 1000);

			
		});
    }


})(jQuery);