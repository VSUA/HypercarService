from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404


def count_position_and_time(queue_of_cars, chosen_service):
    result = {"position": 0, "time": 0}
    for service in queue_of_cars:
        if service != chosen_service:
            result["time"] += len(queue_of_cars[service]) * settings.SERVICES[service]
        else:
            result["time"] += len(queue_of_cars[service]) * settings.SERVICES[service]
            queue_position = 0
            for service_name in settings.SERVICES:
                queue_position += len(queue_of_cars[service_name])
            queue_of_cars[service].append(queue_position + 1)
            result["position"] += queue_position + 1
            break

    return result


def next_ticket_number(queeu_of_services):
    for service in queeu_of_services:
        if len(queeu_of_services[service]) == 0:
            continue
        else:
            return queeu_of_services[service].pop(0)
    return 0


services_queue = {"change_oil": [], "inflate_tires": [], "diagnostic": []}


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello')


class MenuView(View):
    def get(self, requests, *args, **kwsrgs):
        return render(requests, "tickets/menu.html")


class ServicesView(TemplateView):
    template_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs['service'])
        if kwargs['service'] in settings.SERVICES:
            context = count_position_and_time(services_queue, kwargs["service"])
            self.template_name = "tickets/service.html"
            return context
        else:
            raise Http404


class OperatorMenu(View):
    def get(self, request, *args, **kwargs):
        context = {"change_oil_queue": len(services_queue["change_oil"]), "inflate_tires_queue": len(services_queue["inflate_tires"]), "get_diagnostic_queue": len(services_queue["diagnostic"])}
        return render(request, "tickets/operatormenu.html", context=context)

    def post(self, request, *args, **kwargs):
        print(services_queue)
        NextTicketView.next_ticket = {"number": next_ticket_number(services_queue)}
        print(services_queue)
        return redirect("next/")


class NextTicketView(View):
    next_ticket = {"number": 0}
    def get(self, request, *args, **kwargs):
        return render(request, "tickets/next.html", context=self.next_ticket)
