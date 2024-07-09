import asyncio
import traceback

from celery import shared_task
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .services import ChatbotService
import logging

logger = logging.getLogger(__name__)

@shared_task
def async_answer_question(question):
    async def run_chatbot():
        chatbot_service = ChatbotService()
        return await chatbot_service.answer_question(question)

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(run_chatbot())


@csrf_exempt
def qa_bot(request):
    if request.method == 'POST':
        try:
            question = request.POST.get('question')
            logger.info(f"Received question: {question}")

            # Run the chatbot task asynchronously
            task = async_answer_question.delay(question)
            answer, context = task.get()  # This will block until the task is complete

            if answer and context:
                logger.info("Generated answer successfully")
                return JsonResponse({"answer": answer, "context": context})
            else:
                logger.warning("Unable to generate an answer")
                return JsonResponse({"error": "Unable to find information about the specified company"}, status=404)

        except Exception as e:
            logger.error(f"Error in qa_bot: {str(e)}")
            logger.error(traceback.format_exc())
            return JsonResponse({"error": "An unexpected error occurred"}, status=500)

    elif request.method == 'GET':
        return render(request, 'qa_interface.html')

    else:
        return HttpResponse(status=405)  # Method Not Allowed