!(function(context) {
    if (typeof context.ledge === "undefined") {
        context.ledge = {};
    }

    var useTopicLabel = function (input_options) {
        var options = $.merge(input_options, {
            'form': "form",
            'select': "select",
            'container': ".container",
            'inputbox': ".input",
            'button': ".btn"
        });
        var form = options.form;
        var selectField = options.select;
        var labelContainer = options.container;
        var addLabelInput = options.inputbox;
        var addLabelBtn = options.button;

        var addRelatedTopicLabel = function(topicName) {
            // validate input
            if (!topicName) {
                // avoid empty
                alert("请输入话题名称"); // TODO
                return false;
            } else if (topics.indexOf(topicName) === -1) {
                // avoid invalid
                alert("话题\"" + topicName + "\" 不存在"); // TODO
                return false;
            }

            var removeBtn = $('<a>').html("&times;")
                    .attr("class", "remove-topic-btn close")
                    .attr("href", "#");
            var label = $("<span>").text(topicName)
                    .attr("class", "label label-topic")
                    .attr("data-topic-name", topicName)
                    .append(removeBtn);

            // append to topics container
            $(labelContainer).append(label);
            // clear input box
            $(addLabelInput).val("");

            // bind click event of the remove button
            removeBtn.click(function() {
                $(this).parent().fadeOut(function() {
                    $(this).remove();
                });
                return false;
            });
        };


        // get the autocomplete list
        var topics = [];
        $(selectField + " option").each(function() {
            topics.push($(this).text());
        });
        // turn on the autocomplete
        $(addLabelInput).typeahead({source: topics});

        // the click event of adding a related topic
        $(addLabelBtn).click(function() {
            addRelatedTopicLabel($(addLabelInput).val())
        });

        $(selectField).children().each(function () {
            if (typeof $(this).attr("selected") !== "undefined") {
                addRelatedTopicLabel($(this).text());
            }
        });

        // before submit
        $(form).submit(function () {
            $(selectField).children().removeAttr("selected");
            $(labelContainer + " span").each(function() {
                var value = $(this).attr("data-topic-name");
                $(selectField).children().each(function() {
                    if (value === $(this).text()) {
                        $(this).attr("selected", "selected");
                    }
                });
            });
        });
    };

    context.ledge.useTopicLabel = useTopicLabel;
})(this);
