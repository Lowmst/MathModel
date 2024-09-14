function [x_t, y_t, z_t] = coord2xyz(long, lat, height)
    base_long = 110;
    base_lat = 27;
    x_t = (long - base_long) * 97.304;
    y_t = (lat - base_lat) * 111.263;
    z_t = height / 1000;
end