from get_tweet_for_propose import get_tweetList_for_propose
from output import get_output_topics
from arrange_output_and_extract_for_question import arrange_output_and_extract_for_question
import sys

def make_for_experiment(user_name):
    print('Making TweetList...')
    tweetList = get_tweetList_for_propose(screen_name=user_name)
    print('Selecting Topics...')
    output = get_output_topics(tweetList)
    arrange_output_and_extract_for_question(output,tweetList)


if __name__ == '__main__':
    user_name = sys.argv[1]
    make_for_experiment(user_name)
