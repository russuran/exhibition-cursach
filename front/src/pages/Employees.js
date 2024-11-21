import React, { useEffect, useState } from 'react';
import { Table, Button, Modal } from 'antd';
import axios from 'axios';
import EmployeeForm from '../components/EmployeeForm';

const Employees = () => {
    const [employees, setEmployees] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [currentEmployee, setCurrentEmployee] = useState(null);

    useEffect(() => {
        fetchEmployees();
    }, []);

    const fetchEmployees = async () => {
        const response = await axios.get('http://localhost:5000/employees/');
        setEmployees(response.data);
    };

    const handleDelete = async (employeeId) => {
        await axios.delete(`http://localhost:5000/employees/${employeeId}`);
        fetchEmployees();
    };

    const handleModalOpen = (employee) => {
        setCurrentEmployee(employee);
        setIsModalVisible(true);
    };

    const handleModalClose = () => {
        setCurrentEmployee(null);
        setIsModalVisible(false);
    };

    const handleFormSubmit = async (values) => {
        if (currentEmployee) {
            await axios.put(`http://localhost:5000/employees/${currentEmployee.employee_id}`, values);
        } else {
            await axios.post('http://localhost:5000/employees/', values);
        }
        fetchEmployees();
        handleModalClose();
    };

    return (
        <div>
            <Button type="primary" onClick={() => handleModalOpen(null)} style={{ marginBottom: 16 }}>
                Добавить сотрудника
            </Button>
            <Table dataSource={employees} rowKey="employee_id">
                <Table.Column title="ФИО" dataIndex="full_name" />
                <Table.Column title="Должность" dataIndex="position" />
                <Table.Column title="Номер телефона" dataIndex="phone_number" />
                <Table.Column title="Заработная плата" dataIndex="salary" />
                <Table.Column title="Действия" render={(text, employee) => (
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <Button onClick={() => handleModalOpen(employee)}>Редактировать</Button>
                        <Button onClick={() => handleDelete(employee.employee_id)}>Удалить</Button>
                    </div>
                )} />
            </Table>
            <Modal
                title={currentEmployee ? "Редактировать сотрудника" : "Добавить сотрудника"}
                visible={isModalVisible}
                onCancel={handleModalClose}
                footer={null}
            >
                <EmployeeForm
                    initialValues={currentEmployee}
                    onSubmit={handleFormSubmit}
                />
            </Modal>
        </div>
    );
};

export default Employees;
