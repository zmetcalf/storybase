/**
 * Namespace and globals for the story viewer Backbone application
 */
Namespace('storybase.viewer');
storybase.viewer.globals = {};
storybase.viewer.collections = {};
storybase.viewer.models = {};
storybase.viewer.views = {};
storybase.viewer.routers = {};
storybase.viewer.templates = {};
storybase.viewer.utils = {
  max: function(array) {
    return Math.max.apply(Math, array);
  },

  min: function(array) {
    return Math.min.apply(Math, array);
  }
};
