import re

from tqdm import tqdm


def main():
    sensors = {}
    with open("inputs/day15.txt") as f:
        for line in f.readlines():
            pattern = re.compile(r".*x=(-?[0-9]+).*y=(-?[0-9]+).*x=(-?[0-9]+).*y=(-?[0-9]+)")
            sensor_x, sensor_y, beacon_x, beacon_y = map(int, pattern.match(line).groups())
            sensors[f"{sensor_x}_{sensor_y}"] = f"{beacon_x}_{beacon_y}"

    for line_y in tqdm(range(0, 4_000_000)):
        intervals = []
        for sensor, beacon in sensors.items():
            sensor_x, sensor_y = map(int, sensor.split("_"))
            beacon_x, beacon_y = map(int, beacon.split("_"))
            distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
            step = distance - abs(line_y - sensor_y)
            if step >= 0:
                intervals.append((sensor_x - step, sensor_x + step))

        intervals = sorted(intervals, key=lambda x: x[0])
        i = 0
        while i < len(intervals) - 1:
            if intervals[i][1] < intervals[i + 1][0]:
                i += 1
            else:
                intervals[i] = min(intervals[i][0], intervals[i + 1][0]), max(intervals[i][1], intervals[i + 1][1])
                del intervals[i + 1]

        if len(intervals) > 1:
            for i in range(1, len(intervals)):
                if 1 <= intervals[i][0] <= 4_000_000:
                    return (intervals[i][0] - 1) * 4_000_000 + line_y
                elif 0 <= intervals[i - 1][1] < 4_000_000:
                    return (intervals[i - 1][1] + 1) * 4_000_000 + line_y


if __name__ == "__main__":
    print(main())
