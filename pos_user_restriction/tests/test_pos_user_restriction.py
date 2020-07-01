from odoo.tests.common import TransactionCase


class TestUserRestriction(TransactionCase):

    def setUp(self):
        super(TestUserRestriction, self).setUp()
        self.pos_user = self.env['res.users'].create({
            'login': 'pos_user',
            'name': 'pos_user',
            'groups_id': [(6, 0, [self.env.ref('point_of_sale.group_pos_user').id])]
        })
        self.pos_user_assigned_pos = self.env['res.users'].create({
            'login': 'pos_user_assigned_pos',
            'name': 'pos_user_assigned_pos',
            'groups_id': [(6, 0, [self.env.ref(
                'pos_user_restriction.group_assigned_points_of_sale_user').id])]
        })
        self.pos_config_main = self.env.ref('point_of_sale.pos_config_main')
        self.pos_config_model = self.env['pos.config']

    def test_access_pos(self):
        # assigned_user_ids is not set: both users can read
        pos_configs = self.pos_config_model.sudo(self.pos_user.id).search([])
        self.assertTrue(pos_configs)
        pos_configs = self.pos_config_model.sudo(
            self.pos_user_assigned_pos.id).search([])
        self.assertTrue(pos_configs)

        self.pos_config_main.assigned_user_ids = [
            (6, 0, [self.pos_user_assigned_pos.id])]
        # assigned_user_ids is set with pos_user_assigned_pos: both users can read
        pos_configs = self.pos_config_model.sudo(self.pos_user.id).search([])
        self.assertTrue(pos_configs)
        pos_configs = self.pos_config_model.sudo(
            self.pos_user_assigned_pos.id).search([])
        self.assertTrue(pos_configs)

        self.pos_config_main.assigned_user_ids = [
            (6, 0, [self.pos_user.id])]
        # assigned_user_ids is set with pos_user: only pos_user can read
        pos_configs = self.pos_config_model.sudo(self.pos_user.id).search([])
        self.assertTrue(pos_configs)
        pos_configs = self.pos_config_model.sudo(
            self.pos_user_assigned_pos.id).search([])
        self.assertFalse(pos_configs)
