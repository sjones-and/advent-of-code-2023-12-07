#!/usr/bin/env python3

import os
from time import perf_counter_ns

trans_table = str.maketrans('AKQTJ', 'DCBA1')

def get_groups(hand):
    sorted_hand = ''.join(sorted(hand))
    group = None
    groups = []
    for char in sorted_hand:
        if char != '1':
            if not group:
                group = char
            elif group[-1] == char:
                group += char
            else:
                groups.append(group)
                group = char
    groups.append(group or '')
    return sorted(groups, key=len, reverse=True)

def get_hand_value(line):
    raw_hand, bid_value = line.split(' ')
    hand = raw_hand.translate(trans_table)
    groups = get_groups(hand)
    max_group_length = len(groups[0])
    max_group_length += (5 - len(hand.replace('1','')))
    if max_group_length == 5:
        hand_value = 7
    elif max_group_length == 4:
        hand_value = 6
    elif max_group_length == 3:
        if len(groups) == 2:
            hand_value = 5
        else:
            hand_value = 4
    elif max_group_length == 2:
        if len(groups) == 3:
            hand_value = 3
        else:
            hand_value = 2
    else:
        hand_value = 1

    hand_value = int(f'0x{hand_value}{hand}', 16)
    return hand_value, int(bid_value), raw_hand

def answer(input_file):
    start = perf_counter_ns()
    with open(input_file, 'r') as input:
        data = input.read().split('\n')

    hands = sorted([get_hand_value(line) for line in data])
    answer = 0
    for ix in range(len(hands)):
        answer += (ix+1) * hands[ix][1]

    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
