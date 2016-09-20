/**
 * A function to generate tabs for a list of LI elements
 *
 * @param categories a hash that contains {tab name: [list of ids of elements to display]}
 * @param selected   the name of the selected tab (which will not display as a link)
 * @param selector   a jquery element where the tabs should display
 */
function displayCategories(categories, selected, selector) {
    var elem = selector;
    elem.empty();
    elem.append(' | ');
    $.each(categories, function(i, e) {
        if (i === selected) {
            elem.append('<span>' + i + '</span> | ');
            return;
        }
        a = $('<a href="#">').text(i).click(function() {
            $('li').hide();
            var j;
            $.each(e, function(i, e) {
                $('#' + e).show();
            });
            displayCategories(categories, i, selector);
            return false;
        });
        elem.append($('<span>').append(a));
        elem.append(' | ');
    });
}
