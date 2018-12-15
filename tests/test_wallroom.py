
import wallroom


def test_get_sizes():
    r = wallroom.get_sizes()
    assert isinstance(r, set)
    assert '1920x1080' in r


def test_get_images():
    r = wallroom.get_images(size='1920x1080')
    assert(r, list)
    assert(r[0].startswith('/1920x1080'))
