from lettuce import before, step, world
from lettuce.django import django_url
from nose.tools import assert_equal
from splinter.exceptions import ElementDoesNotExist
from storybase_user.models import create_organization, Organization, Project

@before.each_scenario
def setup_organization(scenario):
    matching_scenarios = ('Admin can create a new Project',)
    if scenario.name in matching_scenarios: 
        create_organization("Mile High Connects") 

@step(u'Then the Project named "([^"]*)" should have a canonical URL')
def project_canonical_url(step, name):
    project = Project.objects.get(projecttranslation__name=name)
    world.browser.visit(django_url('/projects/%s' % project.project_id))

@step(u'Then the Project\'s name should be "([^"]*)"')
def see_project_name(step, name):
    world.assert_text_present(name)

@step(u'Then "([^"]*)" should be listed in the Project\'s Organizations list')
def org_in_list(step, org_name):
    world.assert_text_in_list('.grid_3.omega ul li', org_name)

@step(u'Then the Project\'s stories list should be blank')
def no_stories_list(step):
    world.assert_text_not_present("Recent Stories")
    world.assert_text_not_present("Featured Stories")
    assert_equal(len(world.browser.find_by_css('.story-list')), 0)

@step(u'Then the Project\'s description should be blank')
def blank_description(step):
    assert_equal(world.browser.find_by_css('.summary').length, 0)

@step(u'Given the user visits the admin edit page for Project "([^"]*)"')
def visit_admin_edit_page(step, name):
    world.browser.visit(django_url('/admin/storybase_user/project/'))
    world.browser.click_link_by_text(name)
    try:
        # Django 1.3
        project_id = world.browser.find_by_css('.project_id p').first.value
    except ElementDoesNotExist:
        # Django 1.4
        project_id = world.browser.find_by_css('.field-project_id p').first.value

    world.save_info('Project', project_id)

@step(u'Given the user navigates to the Project\'s detail page')
def visit_detail_page(step):
    world.browser.visit(django_url('/projects/%s' % world.project.project_id))

@step(u'Then the Project\'s description is listed as the following:')
def see_description(step):
    world.assert_text_present(step.multiline)

@step(u'Then all other fields of the Project are unchanged')
def other_fields_unchanged(step):
    """ Check that the an organization's fields are unchanged """
    project = Project.objects.get(project_id=world.project.project_id)
    for field in ('project_id', 'website_url', 'description', 'created'):
        if field not in world.project_changed:
            assert_equal(getattr(world.project, field),
                getattr(project, field))

@step(u'Given the user navigates to the Project\'s "([^"]*)" detail page')
def visit_translated_detail_page(step, language):
    world.browser.visit(django_url('/%s/projects/%s' % (world.language_lookup(language), world.project.project_id)))


@step(u'Then the "([^"]*)" Project\'s created on field should be set to the current date')
def project_created_today(step, name):
    project = Project.objects.get(projecttranslation__name=name)
    world.assert_today(project.created)

@step(u'Then the "([^"]*)" Project\'s last edited field should be set to within 1 minute of the current date and time')
def project_edited_now(step, name):
    project = Project.objects.get(projecttranslation__name=name)
    world.assert_now(project.last_edited, 60)

@step(u'Given the Organization "([^"]*)" has been associated with the Project "([^"]*)"')
def associate_org_with_project(step, org_name, project_name):
    org = Organization.objects.get(organizationtranslation__name=org_name)
    project = Project.objects.get(projecttranslation__name=project_name)
    try:
        Project.organizations.through.objects.get(organization=org, project=project)
    except Project.organizations.through.DoesNotExist:
        project.organizations.add(org)
