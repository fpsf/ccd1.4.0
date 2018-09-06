import datetime
import math
from datetime import timedelta

import ephem

from src.business.configuration.configProject import ConfigProject


def result():
    config = ConfigProject()

    info = config.get_geographic_settings()
    infosun = config.get_moonsun_settings()

    max_solar_elevation = float(infosun[0])
    max_lunar_elevation = float(infosun[2])
    max_lunar_phase = float(infosun[3])
    ignorar_lua = infosun[1]

    now_datetime = datetime.datetime.utcnow().replace(hour=12).replace(minute=00).replace(second=0)
    obs = ephem.Observer()

    obs.lat = info[0]
    obs.lon = info[1]
    # Valor Padrão?
    obs.elevation = float(info[2])
    obs.date = ephem.date(now_datetime)

    sun = ephem.Sun()
    sun.compute(obs)
    moon = ephem.Moon()
    moon.compute(obs)
    j = 0
    flag = 0
    ephem_out = False

    while not ephem_out:

        obs.date = ephem.date(now_datetime)
        sun = ephem.Sun()
        sun.compute(obs)

        moon = ephem.Moon()
        moon.compute(obs)
        frac = float(moon.moon_phase) * 100.0

        ag_s = float(repr(sun.alt))
        s_ag = math.degrees(ag_s)
        ag_m = float(repr(moon.alt))
        m_ag = math.degrees(ag_m)

        if ignorar_lua:
            if (float(s_ag) <= max_solar_elevation) and (flag == 0):
                flag = 1
                start = now_datetime
            if (float(s_ag) > max_solar_elevation) and (flag == 1):
                flag = 0
                end = now_datetime
                ephem_out = True
        else:
            if (frac < max_lunar_phase):

                if (float(s_ag) <= max_solar_elevation) and (float(m_ag) <= max_lunar_elevation) and (flag == 0):
                    flag = 1
                    start = now_datetime
                if (float(s_ag) > max_solar_elevation or float(m_ag) > max_lunar_elevation) and (flag == 1):
                    flag = 0
                    end = now_datetime
                    ephem_out = True
            else:
                if (float(s_ag) <= max_solar_elevation) and (float(m_ag) <= float(5.0)) and (flag == 0):
                    flag = 1
                    start = now_datetime
                if (float(s_ag) > max_solar_elevation or float(m_ag) > float(5.0)) and (flag == 1):
                    flag = 0
                    end = now_datetime
                    ephem_out = True
        now_datetime = datetime.datetime.utcnow().replace(hour=12).replace(minute=00).replace(second=0) + timedelta(
            minutes=j)

        j += 1

    obs_time = end - start

    return start, end, obs_time

'''def result():
        config = ConfigProject()

        info = config.get_geographic_settings()
        infosun = config.get_moonsun_settings()

        max_solar_elevation = float(infosun[0])  # -12
        max_lunar_elevation = float(infosun[2])  # 8
        # max_lunar_phase = infosun[3]

        now_datetime = datetime.datetime.utcnow().replace(hour=12).replace(minute=00).replace(second=0)
        obs = ephem.Observer()

        obs.lat = info[0]
        obs.lon = info[1]
        obs.elevation = float(info[2])
        obs.date = ephem.date(now_datetime)

        sun = ephem.Sun()
        sun.compute(obs)
        moon = ephem.Moon()
        moon.compute(obs)
        j = 0
        flag = 0
        for i in range(1, 3000):

            obs.date = ephem.date(now_datetime)
            sun = ephem.Sun()
            sun.compute(obs)

            moon = ephem.Moon()
            moon.compute(obs)
            frac = moon.moon_phase

            ag_s = float(repr(sun.alt))
            s_ag = math.degrees(ag_s)
            ag_m = float(repr(moon.alt))
            m_ag = math.degrees(ag_m)

            if float(s_ag) < max_solar_elevation and float(m_ag) < max_lunar_elevation:
                if flag == 0:
                    flag = 1
                    start = now_datetime
            elif (float(s_ag) > max_solar_elevation or float(m_ag) > max_lunar_elevation) and flag == 1:
                flag = 0
                end = now_datetime
                break

            now_datetime += timedelta(minutes=j)

            j += 1

        obs_time = end - start

        return start, end, obs_time'''

def print_infos():
    info_start_end = result()
    start_time = str(info_start_end[0])
    start_field = "Start: " + start_time[:-10] + " UTC"
    end_time = str(info_start_end[1])
    end_field = "End: " + end_time[:-10] + " UTC"
    time_obs_time = str(info_start_end[2])
    time_obs_field = "Total Obs. Time:" + time_obs_time[:-10] + " Hours"
    print(start_field)
    print(end_field)
    print(time_obs_field)
