#!/usr/bin/python
# -*- coding: utf-8 -*-
import redis

red = redis.StrictRedis(host='localhost', port=6379, db=0)


if __name__ == "__main__":
    red.set('a','abc')
    print red.get('a')