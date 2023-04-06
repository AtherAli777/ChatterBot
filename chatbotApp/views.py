# Import necessary libraries and models
import openai
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Past
from django.core.paginator import Paginator

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

# Define home function
def home(request):
    # Check if form has been submitted
    if request.method == 'POST':
        # Fetch user query and past responses from form data
        query = request.POST['query']
        past_responses = request.POST['past_responses']

        try:
            # Test OpenAI authentication by listing models
            openai.Model.list()

            # Get response from OpenAI using the text-davinci-003 engine
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=query,
                temperature=0,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )

            # Extract text response from API result
            response = (response['choices'][0]['text']).strip()

            # Append new response to past_responses variable
            if not past_responses:
                past_responses = response
            else:
                past_responses = f"{past_responses} <br/><br/>  {response}"
            
            # Record the question and answer in the database
            record = Past(question=query, answer=response)
            record.save()
            
        except Exception as e:
            # Handle OpenAI API errors
            response = f"An error occurred: {e}"
            past_responses = ""

        # Render the home page with query, response, and past responses
        return render(request, 'index.html', {'query': query, 'response': response, 'past_responses': past_responses})

    # Render the home page with empty context
    return render(request, 'index.html',{})

# Define past function
def past(request):
    # Set up paginator to display Past objects in groups of 10
    p = Paginator(Past.objects.all(), 10)

    # Determine current page from URL parameter or default to page 1
    if 'page' in request.GET and request.GET['page']:
        page = request.GET.get('page')
    else:
        page = 1

    # Get the specified page from the paginator
    pages = p.get_page(page)

    # Retrieve all Past objects from the database
    past = Past.objects.all()

    # Generate a string of characters to display page numbers
    nums = "a" * pages.paginator.num_pages

    # Render the past page with past data, page data, and page number characters
    return render(request, 'past.html', {'past': past, 'pages': pages, 'nums': nums})

# Define delete function
def delete(request, list_id):
    # Retrieve the specified Past object from the database
    past = Past.objects.get(pk=list_id)

    # Delete the Past object from the database
    past.delete()

    # Redirect to the past page
    return redirect('past')
