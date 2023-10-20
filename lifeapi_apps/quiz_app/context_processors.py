# making variables available in ALL requests

def data_table_test_status(request):
    # Check if the user is a member of the "data_table_test" group
    is_data_table_test_member = request.user.groups.filter(name='data_table_test').exists()

    # print(is_data_table_test_member)

    return {
        'is_data_table_test_member': is_data_table_test_member,
    }