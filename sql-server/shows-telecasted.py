from datetime import datetime, timedelta


def shows_telecast():

    test_cases = int(input("\nPlease Enter The No Of Test Cases : \n"))
    final_show_diff_times = []
    show_diff_time_result = []
    FMT = '%H:%M:%S'

    try:

        if test_cases or test_cases is int() and test_cases > 0:
            for test in range(test_cases):
                no_of_shows = int(input("\nPlease Enter the No Of Shows for {} Case : \n".format(test+1)))

                if no_of_shows or no_of_shows is int() and no_of_shows > 0:

                    for show in range(no_of_shows):

                        start_time = input("Please Enter The Start Time for {} Show of {} Case "
                                           "(HH:MM:SS)\n".format(show + 1, test + 1))
                        end_time = input("Please Enter The End Time for {} Show of {} Case "
                                         "(HH:MM:SS)\n".format(show + 1, test + 1))

                        show_diff_time = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)
                        show_diff_time_result.append(show_diff_time)
                else:
                    print("Please Enter The Correct Show Case Count")

                final_show_diff_times.append(show_diff_time_result)

        else:
            print("\nPlease Enter The Correct Test Case Count")

        return show_diff_time_result

    except Exception as EX:
        print("Exception Encountered : {}".format(EX))


shows_telecast_time_diff = shows_telecast()


# HINT: To get the time delta in seconds you have to call shows_telecast_time_diff.total_seconds()

for difference in shows_telecast_time_diff:
    if difference.days < 0:
        difference = timedelta(
            days=0, seconds=difference.seconds, microseconds=difference.microseconds)
    print(difference)
    # print(difference.total_seconds(), difference.microseconds)

