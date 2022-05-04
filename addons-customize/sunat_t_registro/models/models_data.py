from odoo import api, fields, models
from odoo.osv import expression


class IndustrialClasification(models.Model):
    _name = 'international.industrial.classification'
    _description = 'Clasificación Industrial'

    code = fields.Char(string='Código CIIU')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class AccountMove(models.Model):
    _inherit = 'hr.contract'

    displacemnent = fields.Boolean(string='Destaco o Desplazo')
    employer_id = fields.Many2one(comodel_name='res.partner', string='Empleador')
    date_from_displacement = fields.Date(string='Fecha de Inicio')
    date_to_displacement = fields.Date(string='Fecha de Fin')
    risk_activities = fields.Boolean(string='Actividades de riesgo')
    given_service = fields.Many2one(comodel_name='international.industrial.classification', string='Servicio Prestado')
    worker_type_pensioner_provider = fields.Many2one(comodel_name='worker.type.pensioner.provider',
                                                     string='Tipo de trabajador, penionista o prestador de servicios')


class RoadTypeObject(models.Model):
    _name = "road.type.object"

    code = fields.Char(string='N°')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class ZoneTypeObject(models.Model):
    _name = "zone.type.object"

    code = fields.Char(string='N°')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class UbigeoReniecObject(models.Model):
    _name = "ubigeo.reniec.object"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    road_type = fields.Many2one('road.type.object', string='Tipo de Vía')
    road_name = fields.Char(string='Nombre de Vía')
    road_number = fields.Char(string='Número de Vía')
    road_departament = fields.Char(string='Departamento')
    road_inside = fields.Char(string='Interior')
    road_mz = fields.Char(string='Manzana')
    road_batch = fields.Char(string='Lote')
    road_km = fields.Char(string='Kilómetro')
    road_block = fields.Char(string='Block')
    road_stage = fields.Char(string='Etapa')
    zone_type = fields.Many2one('zone.type.object', string='Tipo de Zona')
    zone_name = fields.Char(string='Nombre de Zona')
    zone_reference = fields.Char(string='Referencia')
    zone_ubigeo = fields.Many2one('ubigeo.reniec.object', string='Ubigeo')

    address_2 = fields.Boolean(string='Dirección 2')

    indicator_essalud = fields.Selection(string='Indicador Centro Asistencial EsSalud', selection=[
        ('01', 'Dirección 1'),
        ('02', 'Dirección 2'),
    ])

    road_type_2 = fields.Many2one('road.type.object', string='Tipo de Vía')
    road_name_2 = fields.Char(string='Nombre de Vía')
    road_number_2 = fields.Char(string='Número de Vía')
    road_departament_2 = fields.Char(string='Departamento')
    road_inside_2 = fields.Char(string='Interior')
    road_mz_2 = fields.Char(string='Manzana')
    road_batch_2 = fields.Char(string='Lote')
    road_km_2 = fields.Char(string='Kilómetro')
    road_block_2 = fields.Char(string='Block')
    road_stage_2 = fields.Char(string='Etapa')
    zone_type_2 = fields.Many2one('zone.type.object', string='Tipo de Zona')
    zone_name_2 = fields.Char(string='Nombre de Zona')
    zone_reference_2 = fields.Char(string='Referencia')
    zone_ubigeo_2 = fields.Many2one('ubigeo.reniec.object', string='Ubigeo')


class ResCountry(models.Model):
    _inherit = 'res.country'

    cod_pas_only = fields.Char(string='Código sólo para pasaporte')
    nacionality_code_rc = fields.Char(string='Código de Nacionalidad')


class OccupationalWorkerCategory(models.Model):
    _name = "occupational.worker.category"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')
    private_sector = fields.Char(string='Sector Privado')
    public_sector = fields.Char(string='Sector Público')
    other_entities = fields.Char(string='Otras Entidades')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class WorkerTypePensionerProvider(models.Model):
    _name = "worker.type.pensioner.provider"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')
    abbreviated_name = fields.Char(string='Descripción abreviada')
    private_sector = fields.Char(string='Sector Privado')
    public_sector = fields.Char(string='Sector Público')
    other_entities = fields.Char(string='Otras Entidades')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class HrContract(models.Model):
    _inherit = 'hr.contract'

    periodicity = fields.Selection(string='Periodicidad', selection=[
        ('01', 'Mensual'),
        ('02', 'Quincenal'),
        ('03', 'Semanal'),
        ('04', 'Diaria'),
        ('05', 'Otros'),
    ])
    work_category = fields.Many2one('occupational.worker.category', string='Categoría ocupacional del trabajado')
    type_formative_modality = fields.Many2one('type.formative.modality.work', string='Tipo de modalidad formativa laboral')
    occupation_training_modality = fields.Many2one('occupation.work.personnel.training.modality', string='Ocupación de trabajo')
    health_insurance_contract = fields.Selection(string='Seguro médico', selection=[
        ('01', 'Essalud'),
        ('02', 'Privado'),
    ])
    mother_responsability = fields.Boolean(string="Madre con responsabilidad Familiar")
    type_professional_center = fields.Selection(string='Tipo de Centro de Formación Profesional', selection=[
        ('01', 'Centro educativo'),
        ('02', 'Universidad'),
        ('03', 'Instituto'),
        ('04', 'Otros'),
    ])


class Employee(models.Model):
    _inherit = 'hr.employee'

    situation = fields.Selection(string='Situación', selection=[
        ('0', 'Baja'),
        ('1', 'Activo o subsidiado'),
        ('2', 'Sin vínculo laboral con conceptos pendiente de liquidar'),
        ('3', 'Suspensión perfecta de labores'),
    ])
    sctr = fields.Selection(string='SCTR', selection=[
        ('0', 'Ninguno'),
        ('1', 'ONP'),
        ('2', 'Cía. privada'),
    ])
    rent_category = fields.Boolean(string="Rentas de 5ta categoría exoneradas")
    double_taxation = fields.Selection(string='Convenio para evitar la doble tributación', selection=[
        ('0', 'Ninguno'),
        ('1', 'Canada'),
        ('2', 'Chile'),
        ('3', 'Can'),
        ('4', 'Brasil'),
    ])
    category_employee = fields.Selection(string='Categoria de Empleado', selection=[
        ('1', 'Trabajador'),
        ('2', 'Pensionista'),
        ('4', 'Personal de terceros'),
        ('5', 'Personal en formacion'),
    ], default='1')
    eps_services_propios = fields.Selection(string='EPS/Servicios Propios', selection=[
        ('1', '20514372251   -   PERSALUD S.A. EPS (1)'),
        ('2', '20431115825   -   PACÍFICO S.A. EPS'),
        ('3', '20414955020   -   RÍMAC INTERNACIONAL S.A. EPS'),
        ('4', '0             -   SERVICIOS PROPIOS'),
        ('5', '20517182673   -   MAPFRE PERU S.A. EPS'),
        ('6', '20523470761   -   SANITAS PERU S.A. - EPS'),
        ('7', '20601978572   -   EPS, LA POSITIVA S.A. ENTIDAD PRESTADORA DE SALUD'),
    ], default='1')
    sctr_salud = fields.Selection(string='SCTR SALUD', selection=[
        ('1', 'Essalud'),
        ('2', 'EPS'),
    ])
    inv_eps = fields.Char(related='health_regime_id.code')
    edu_inst = fields.Selection(string='Institución Educativa del Perú', selection=[
        ('si', 'SI'),
        ('no', 'NO'),
    ])
    edu_name_id = fields.Many2one('edu.name.object', string='Institución Educativa')
    edu_career_id = fields.Many2one('edu.career.object', string='Carrera')
    edu_year_id = fields.Many2one('edu.year.graduation.object', string='Año de Graduación')
    edu_bool = fields.Char(related='academic_degree_id.code')


class EduNameObject(models.Model):
    _name = "edu.name.object"
    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class EduCareerObject(models.Model):
    _name = "edu.career.object"
    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class EduYearGraduationObject(models.Model):
    _name = "edu.year.graduation.object"
    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class TypeFormativeModalityWork(models.Model):
    _name = "type.formative.modality.work"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')
    abbreviated_name = fields.Char(string='Descripción abreviada')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class OccupationWorkPersonnelTrainingModality(models.Model):
    _name = "occupation.work.personnel.training.modality"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
