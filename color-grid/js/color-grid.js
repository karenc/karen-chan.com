(function($) {
    $(function() {
        window.currentColor = 'white';

        var Grid = Backbone.Model.extend({
            setColor: function(color) {
                this.color = color;
            }
        });

        var GridTable = Backbone.Collection.extend({
            model: Grid
        });

        var GridView = Backbone.View.extend({
            tagName: 'td',
            model: Grid,
            events: {
                'click': 'clickHandler'
            },
            initialize: function() {
                this.listenTo(this.model, 'change', this.render);
                this.listenTo(this, 'click', this.setColor);
            },
            clickHandler: function() {
                this.model.save({color: window.currentColor});
            },
            render: function() {
                this.$el.css('background-color', this.model.get('color'));
                return this;
            }
        });

        var GridTableView = Backbone.View.extend({
            tagName: 'table',
            render: function() {
                var width = this.options.width;
                var height = this.options.grids.length / width;
                var i, j;
                var grid;
                var tr;
                for (j = 0; j < height; j++) {
                    tr = $('<tr>').appendTo(this.$el);
                    for (i = 0; i < width; i++) {
                        grid = this.options.grids.get(j * width + i);
                        tr.append(new GridView({model: grid}).render().el);
                    }
                }
                return this;
            }
        });

        var ColorPickerView = Backbone.View.extend({
            render: function() {
                $('#color-picker').farbtastic(function(color) {
                    window.currentColor = color;
                });
                return this;
            }
        });

        var AppView = Backbone.View.extend({
            initialize: function() {
                this.grids = new GridTable();
                this.grids.bind('all', this.render, this);
                this.grids.fetch();
            },
            render: function() {
                new ColorPickerView().render();
                this.$el.html('');
                this.$el.append(new GridTableView({grids: this.grids, width: 7}).render().el);
                return this;
            }
        });

        var app = new AppView();
        $('#color-grid').append(app.render().el);
    });

    Backbone.sync = function(method, model, options) {
        options.type = 'GET';
        if (method === 'update') {
            options.type = 'POST';
            options.data = model.toJSON();
        }
        var xhr = options.xhr = $.ajax('cgi-bin/server.cgi?method=' + method, options);
        model.trigger('request', model, xhr, options);
        return xhr;
    };
})(jQuery);
