# -*- coding: utf-8 -*-
#
#  decorators.py
#  kanji_tester
# 
#  Created by Lars Yencken on 13-11-2008.
#  Copyright 2008 Lars Yencken. All rights reserved.
#

from django.http import HttpResponseRedirect
from django.urls import reverse


def profile_required(view_method):
    """
    A decorator which indicates that a user profile is required for the given
    view.
    """
    def maybe_redirect(request):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect(reverse("tutor_welcome")) 

        # print hasattr(user, 'profile')
        if not hasattr(user, 'profile'):  # user.profile.count() == 0:
            return HttpResponseRedirect(reverse("userprofile_profile"))

        return view_method(request)

    return maybe_redirect
