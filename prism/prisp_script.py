def get_final_data_table(*, data, date_from='2019-12-01', date_to='2019-12-31', state='', city='', group_by=''):
    output_data_table = _apply_date_filter(data=data, date_from=date_from, date_to=date_to)
    output_data_table = _apply_state_filter(data=output_data_table, state=state)
    output_data_table = _apply_city_filter(data=output_data_table, city=city)
    output_data_table = _group_by(data=output_data_table, group_by=group_by)

    output_data_table['conversion'] = output_data_table['trials'] / output_data_table['installs']
    output_data_table['conversion'] = [f'{i:.2%}' for i in output_data_table['conversion']]

    return output_data_table


def _apply_date_filter(*, data, date_from, date_to):
    output = data[(data['date'] >= date_from) & (data['date'] <= date_to)]
    return output


def _apply_state_filter(*, data, state: str):
    if len(state) == 0:
        return data
    else:
        state_list = state.split(', ')
        output = data[data['state'].isin(state_list)]
        return output


def _apply_city_filter(*, data, city: str):
    if len(city) == 0:
        return data
    else:
        city_list = city.split(', ')
        output = data[data['city'].isin(city_list)]
        return output


def _group_by(*, data, group_by: str):
    if len(group_by) == 0:
        return data
    else:
        params_list = group_by.split(', ')
        output = data.groupby(by=params_list).sum()
        return output
