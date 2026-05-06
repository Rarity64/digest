let bodyHeight = $(document).height() - $('footer').height();

if($(window).height() == $(document).height()) {
    $('main').css('height', bodyHeight + 'px');
}