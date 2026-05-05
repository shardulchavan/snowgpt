def get_active_behaviors(row):
    lookup_column = ['FOOTBALL_ENTHUSIAST', 'BASEBALL_ENTHUSIAST', 'BASKETBALL_ENTHUSIAST','HOCKEY_ENTHUSIAST', 'SOCCER_ENTHUSIAST', 'TENNIS_ENTHUSIAST','SPORTING_GOODS_BUYER','EXERCISE_CLASS_ENTHUSIAST', 'RUNNING_ENTHUSIAST', 'BICYCLING_ENTHUSIAST']
    result = ''
    for column in lookup_column:
        if column in row and row[column] == 'Y':
            if '_ENTHUSIAST' in column:
                result += column.split('_ENTHUSIAST')[0] + ','
            else:
                result += column + ','
    return result.strip()