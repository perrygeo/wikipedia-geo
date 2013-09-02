-- First `createdb wikipedia-geo`

CREATE EXTENSION postgis;

CREATE TABLE wikigeo
(
  title CHARACTER VARYING(255),
  lon DOUBLE PRECISION,
  lat DOUBLE PRECISION,
  "name" CHARACTER VARYING(255),
  "type" CHARACTER VARYING(50)
);

COPY wikigeo FROM 'output_of_extract_geo.dat'

SELECT AddGeometryColumn ('public','wikigeo','geom',4326,'POINT',2);

UPDATE wikigeo set geom = ST_SetSRID(ST_Point(lon,lat),4326);

CREATE INDEX idx_wikigeo_geom ON wikigeo USING GIST (geom);

ALTER table wikigeo ALTER COLUMN geom SET not null;

CLUSTER wikigeo USING idx_wikigeo_geom;

VACUUM ANALYZE;

-- Test
SELECT title, "type", "name"
FROM wikigeo
WHERE ST_DWithin(ST_GeometryFromText('POINT(-122.7810 45.5429)', 4326), geom, 0.1) -- within 0.1 degrees
limit 150
;
