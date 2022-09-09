import json

import httpx
from assertpy import assert_that
from behave import given, then, when


@given('the base URL is "{base_url}"')
def step_given_base_url(context, base_url):
    context.api.base_url = base_url


@given("I set the headers")
def step_given_set_headers(context):
    context.api.headers = json.loads(context.text)


@when('I make a GET request to "{endpoint}"')
def step_when_get_request(context, endpoint):
    url = f"{context.api.base_url}{endpoint}"
    context.api.response = httpx.get(url, headers=context.api.headers)


@when('I make a POST request to "{endpoint}" with JSON body')
def step_when_post_request(context, endpoint):
    url = f"{context.api.base_url}{endpoint}"
    body = json.loads(context.text)
    context.api.response = httpx.post(url, json=body, headers=context.api.headers)


@when('I make a PUT request to "{endpoint}" with JSON body')
def step_when_put_request(context, endpoint):
    url = f"{context.api.base_url}{endpoint}"
    body = json.loads(context.text)
    context.api.response = httpx.put(url, json=body, headers=context.api.headers)


@when('I make a PATCH request to "{endpoint}" with JSON body')
def step_when_patch_request(context, endpoint):
    url = f"{context.api.base_url}{endpoint}"
    body = json.loads(context.text)
    context.api.response = httpx.patch(url, json=body, headers=context.api.headers)


@when('I make a DELETE request to "{endpoint}"')
def step_when_delete_request(context, endpoint):
    url = f"{context.api.base_url}{endpoint}"
    context.api.response = httpx.delete(url, headers=context.api.headers)


@then("the response status code should be {status_code:d}")
def step_then_status_code(context, status_code):
    assert_that(context.api.response.status_code).is_equal_to(status_code)


@then("the response JSON should contain")
def step_then_response_json(context):
    expected_json = json.loads(context.text)
    response_json = context.api.response.json()
    assert_that(response_json).is_equal_to(expected_json)
