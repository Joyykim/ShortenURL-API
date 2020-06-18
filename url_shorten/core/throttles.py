from rest_framework import throttling


class MembershipThrottle(throttling.UserRateThrottle):
    rate = '60/m'


class UserThrottle(throttling.UserRateThrottle):
    rate = '20/m'


class AnonThrottle(throttling.AnonRateThrottle):
    rate = '10/m'
