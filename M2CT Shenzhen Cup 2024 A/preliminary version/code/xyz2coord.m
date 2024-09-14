function [long, lat, height] = xyz2coord(x, y, z)
    base_long = 110;
    base_lat = 27;
    long = x / 97.304 + base_long;
    lat = y / 111.263 + base_lat;
    height = z * 1000;
end