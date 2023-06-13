from part_1.connect import client
from models import Author, Quote

import redis
from redis_lru import RedisLRU


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client, default_ttl=60*60)


def main():
    while True:
        user_input = parser()

        if user_input == "exit":
            break
        elif user_input == None:
            continue

        command, value = user_input
        print(COMMANDS[command](value))


def exception_handler(func):
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except (ValueError):
            print("Enter one of that command: name:<value>, tag:<value>, tags:<value>,<value>,...")

    return wrapper


@exception_handler
def parser():
    user_input = input("Enter command: ")

    if user_input == "exit":
        return user_input
    
    command, value = user_input.split(":")
    command = command.strip()
    value = value.strip()

    if command not in COMMANDS.keys():
        raise ValueError
    
    return command, value


@cache
def name_search(name):
    result = []
    author = Author.objects(fullname__istartswith=name).first()
    quotes = Quote.objects(author=author.id)
    
    if quotes:
        for quote in quotes:
            result.append(quote.quote)
        result = ", ".join(result)
        return result
    else:
        print("You have no quotes.")


@cache
def tag_search(tag):
    result = []
    quotes = Quote.objects(tags__istartswith=tag)
    
    if quotes:
        for quote in quotes:
            result.append(quote.quote)
        result = ", ".join(result)
        return result
    else:
        print("You have no quotes.")


def tags_search(tags):
    quotes = Quote.objects(tags__in=tags.split(","))
    
    if quotes:
        for quote in quotes:
            print(quote.quote)
    else:
        print("You have no quotes.")


COMMANDS = {
    "name": name_search,
    "tag": tag_search,
    "tags": tags_search,
}


if __name__ == "__main__":
    main()
