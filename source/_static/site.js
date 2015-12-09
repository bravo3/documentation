
$(function() {
    $('.configuration-block ul>li>em').each(function() {
        var title = $(this).text();
        var anchor = $('<a class="cfg-tab" href="javascript://"></a>').text(title).click(function() {
            var ul = $(this).closest('ul');

            ul.find('>li>div').each(function() {
                $(this).css("height", "0px");
            });

            ul.find('li').removeClass('active');
            $(this).parent().parent().addClass('active');

            var h = $(this).parent().parent().children('div').css("height", "auto").outerHeight();
            var base = ul.find('li').outerHeight();

            ul.css("height", (base + h) + "px");
        });
        $(this).empty().append(anchor);
    });

    $('.configuration-block ul>li:first-child>em>a').click();
});
