from unittest import TestCase, main

from q2_gcn_norm.plugin_setup import plugin


class PluginTests(TestCase):

    def test_plugin(self):
        self.assertEqual(plugin.name, 'gcn-norm')


if __name__ == '__main__':
    main()