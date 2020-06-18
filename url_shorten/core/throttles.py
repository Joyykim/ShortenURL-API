from rest_framework import throttling


class MembershipThrottle(throttling.UserRateThrottle):
    rate = '6/m'


class UserThrottle(throttling.UserRateThrottle):
    rate = '4/m'


class AnonThrottle(throttling.AnonRateThrottle):
    rate = '2/m'
