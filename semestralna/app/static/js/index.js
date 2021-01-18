var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    context: document.getElementById('main-body'),
    onBeforePageLoad: function () {
        $('.loading').show();
    },
    onAfterPageLoad: function ($items) {
        $('.loading').hide();
    }
});