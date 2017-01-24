ko.doTEngine = function () { }
ko.doTEngine.prototype = ko.utils.extend(new ko.templateEngine(), {
    renderTemplateSource: function (templateSource, bindingContext, options) {
        var precompiled = templateSource.data('precompiled');
        if (!precompiled) {
            precompiled = doT.template("{{ with(it) { with(it.$data) { }}" + templateSource.text() + "{{ } } }}");
            templateSource.data('precompiled', precompiled);
        }

        var renderedMarkup = precompiled(bindingContext);
        return ko.utils.parseHtmlFragment(renderedMarkup);
    },
    createJavaScriptEvaluatorBlock: function(script) {
        return "{{=" + script + "}}";
    }
});

ko.bindingHandlers.dotTemplate = {
    init: function(element, valueAccessor, allBindings, vm, context) {
        var options = ko.utils.unwrapObservable(valueAccessor());

        if (!options || typeof options !== "object") {
            options = {
                name: valueAccessor()
            };

        }

        options.templateEngine = ko.bindingHandlers.dotTemplate.engine

        ko.applyBindingsToNode(element, {
            template: options
        }, context);

        return { controlsDescendantBindings: true };
    },
    engine: new ko.doTEngine()
}